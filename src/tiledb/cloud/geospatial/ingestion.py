import math
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

import fiona
import laspy
import rasterio
import shapely
from rtree import index

import tiledb
from tiledb.cloud.utilities import Profiler
from tiledb.cloud.utilities import as_batch
from tiledb.cloud.utilities import batch
from tiledb.cloud.utilities import create_log_array
from tiledb.cloud.utilities import find
from tiledb.cloud.utilities import get_logger_wrapper
from tiledb.cloud.utilities import max_memory_usage
from tiledb.cloud.utilities import run_dag

# fiona.drvsupport.supported_drivers["TileDB"] = "rw"
# fiona.vfs.SCHEMES["tiledb"] = "tiledb"

DEFAULT_RESOURCES = {"cpu": "2", "memory": "2Gi"}
DEFAULT_IMG_NAME = "3.9-geo"
DEFAULT_DAG_NAME = "geo-ingestion"

# Default values for ingestion parameters
RASTER_TILE_SIZE = 1024
POINT_CLOUD_CHUNK_SIZE = 1_000_000
MAX_WORKERS = 40
BATCH_SIZE = 10


class DatasetType(Enum):
    POINTCLOUD = 1
    RASTER = 2
    GEOMETRY = 3


@dataclass
class BoundingBox:
    minx: float
    miny: float
    maxx: float
    maxy: float
    minz: Optional[float] = None
    maxz: Optional[float] = None

    @property
    def bounds(self):
        if self.minz:
            return (self.minx, self.miny, self.minz, self.maxx, self.maxy, self.maxz)
        else:
            return (self.minx, self.miny, self.maxx, self.maxy)


@dataclass
class GeoBlockMetadata:
    ranges: Tuple[Tuple[int, int], Tuple[int, int]]
    files: Tuple[os.PathLike, ...]


@dataclass
class GeoMetadata:
    # common properties
    extents: BoundingBox
    crs: str = None
    paths: Optional[Union[List[os.PathLike], os.PathLike]] = None
    # raster properties
    dtype: Optional[str] = (None,)
    band_count: Optional[int] = None
    res: Optional[Tuple[float, float]] = None
    block_metadata: Optional[Tuple[GeoBlockMetadata, ...]] = None
    # point cloud properties
    scales: Optional[Tuple[float, float, float]] = None
    offsets: Optional[Tuple[float, float, float]] = None


def get_pointcloud_metadata(
    sources: Iterable[os.PathLike],
    *,
    config: Mapping[str, Any] = None,
    verbose: bool = False,
    id: str = "pointcloud_metadata",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> GeoMetadata:
    """Return geospatial metadata for a sequence of input point cloud data files

    :param sources: iterator, paths or path to process
    :param config: dict, configuration to pass on tiledb.VFS
    :param verbose: bool, enable verbose logging, default is False
    :param trace: bool, enable trace logging, default is False
    :param log_uri: Optional[str] = None,
    :Return: GeoMetadata, a populated GeoMetadata object
    """
    if len(sources) == 0:
        raise ValueError("Input point cloud datasets required")

    with tiledb.scope_ctx(config):
        vfs = tiledb.VFS()
        logger = get_logger_wrapper(verbose)
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            offsets = None
            scales = None
            mins = None
            maxs = None
            for f in sources:
                logger.debug("finding metadata for %r", f)
                with vfs.open(f, "rb") as src:
                    # only open header
                    las = laspy.open(src)
                    hdr = las.header
                    if mins is None:
                        mins = hdr.mins
                    else:
                        mins = [min(e) for e in zip(mins, hdr.mins)]

                    if maxs is None:
                        maxs = hdr.maxs
                    else:
                        maxs = [max(e) for e in zip(maxs, hdr.maxs)]

                    if scales is None:
                        scales = hdr.scales
                    else:
                        scales = [max(e) for e in zip(scales, hdr.scales)]

                    if offsets is None:
                        offsets = hdr.offsets
                    else:
                        offsets = [min(e) for e in zip(offsets, hdr.offsets)]

            return GeoMetadata(
                paths=sources,
                extents=BoundingBox(
                    minx=mins[0],
                    miny=mins[1],
                    minz=mins[2],
                    maxx=maxs[0],
                    maxy=maxs[1],
                    maxz=maxs[2],
                ),
                scales=tuple(scales),
                offsets=tuple(offsets),
            )


def get_geometry_metadata(
    source: Iterable[os.PathLike],
    config: Mapping[str, Any] = None,
) -> GeoMetadata:
    """Return geospatial metadata for a sequence of input geometry data files

    :param source: A sequence of paths or path to input
    :param config: dict configuration to pass on tiledb.VFS
    """
    # note this will be refactor to use /vsipyopener in fiona
    pass


def get_raster_metadata(
    sources: Iterable[os.PathLike],
    *,
    config: Mapping[str, Any] = None,
    dst_tile_size: [int] = RASTER_TILE_SIZE,
    res: Tuple[float, float] = None,
    verbose: bool = False,
    id: str = "raster_metadata",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> GeoMetadata:
    """Return geospatial metadata for a sequence of input raster data files

    :param sources: iterator, paths or path to process
    :param config: dict, configuration to pass on tiledb.VFS
    :param dst_tile_size: int, tile size of the destination mosaic
    :param verbose: bool, enable verbose logging, default is False
    :param trace: bool, enable trace logging, default is False
    :param log_uri: Optional[str] = None,
    :Return: GeoMetadata, a populated GeoMetadata objects with blocks
             and the files that contribute to each block
    """
    if len(sources) == 0:
        raise ValueError("Input raster datasets required")

    logger = get_logger_wrapper(verbose)
    full_extents = None
    crs = None
    num_bands = None
    do_res_check = True
    dtype = None

    if res:
        xres, yres = res
        do_res_check = False
    else:
        xres = None
        yres = None

    def group_by_raster_block(
        meta: Sequence[GeoMetadata],
    ) -> Tuple[GeoBlockMetadata, ...]:
        nonlocal logger

        # fast bulk load of geometries in to a r-tree
        def load_geoms(meta):
            for i, im in enumerate(meta):
                yield (i, im.extents.bounds, None)

        idx = index.Index(load_geoms(meta))
        bounds = tuple(idx.bounds)
        if bounds != full_extents.bounds:
            logger.error(
                "Index bounds %r Expected bounds %r", bounds, full_extents.bounds
            )
            raise ValueError("Unexpected bounds mismatch in raster ingest")

        width = (bounds[2] - bounds[0]) / xres
        height = (bounds[3] - bounds[1]) / yres
        num_blocks_x = math.ceil(width / dst_tile_size)
        num_blocks_y = math.ceil(height / dst_tile_size)

        dst_transform = rasterio.transform.from_bounds(
            *full_extents.bounds, width, height
        )
        dst_window = rasterio.windows.Window(0, 0, width, height)

        results = []
        for i in range(num_blocks_x):
            for j in range(num_blocks_y):
                # calculate window in local pixel co-ordinates
                # and clamp to destination dimensions
                win = rasterio.windows.Window(
                    i * dst_tile_size, j * dst_tile_size, dst_tile_size, dst_tile_size
                ).intersection(dst_window)
                region_bounds = rasterio.windows.bounds(win, dst_transform)
                # find intersection
                intersects = tuple(idx.intersection(region_bounds))
                if len(intersects) > 0:
                    # append the result in pixel coords
                    results.append(
                        GeoBlockMetadata(
                            ranges=win.toranges(),
                            files=tuple([meta[s].paths for s in intersects]),
                        )
                    )

        return tuple(results)

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            meta = []
            vfs = tiledb.VFS(config=config)

            for pth in sources:
                logger.debug("Including %r", pth)
                extents = None
                with rasterio.open(pth, opener=vfs.open) as src:
                    extents = BoundingBox(
                        minx=src.bounds[0],
                        miny=src.bounds[1],
                        maxx=src.bounds[2],
                        maxy=src.bounds[3],
                    )
                    logger.debug("Extents for %r %r", pth, extents)

                    # initialization of variables
                    if crs is None:
                        crs = src.crs
                    else:
                        if crs != src.crs:
                            raise ValueError(
                                "All datasets need to be in the same projection"
                            )

                    if num_bands is None:
                        num_bands = src.count
                    else:
                        if num_bands != src.count:
                            raise ValueError(
                                "All datasets need to have the same number of bands"
                            )

                    if dtype is None:
                        dtype = src.profile["dtype"]
                    else:
                        if dtype != src.profile["dtype"]:
                            raise ValueError(
                                "All datasets need to have the same data type"
                            )

                    if do_res_check:
                        # first input resolution is used
                        # if not specified as an input arg
                        if xres is None:
                            xres, yres = src.res
                        else:
                            if xres != src.res[0] or yres != src.res[1]:
                                raise ValueError(
                                    """All datasets need to have the same resolution "
                                    if target resolution is not specified"""
                                )

                if full_extents:
                    full_extents = BoundingBox(
                        *shapely.unary_union(
                            [
                                shapely.box(*full_extents.bounds),
                                shapely.box(*extents.bounds),
                            ]
                        ).bounds
                    )
                else:
                    full_extents = extents

                meta.append(
                    GeoMetadata(
                        paths=pth,
                        extents=extents,
                        crs=crs,
                    )
                )
            if len(meta) > 0:
                blocks = group_by_raster_block(meta)
                return GeoMetadata(
                    block_metadata=blocks,
                    crs=crs,
                    extents=full_extents,
                    res=(xres, yres),
                    band_count=num_bands,
                    dtype=dtype,
                )
            else:
                raise ValueError("Raster datasets not found")


def ingest_geometry_udf(
    sources: Optional[Sequence[str]],
    dataset_uri: str,
    *args: Any,
    **kwargs,
):
    """Internal udf that ingests server side batch of geometry files
    into tiledb arrays using Fiona API

    :param input: raster input file names
    :param output: output TileDB array name
    """
    pass


def ingest_point_cloud_udf(
    sources: Optional[Sequence[str]] = None,
    *,
    dataset_uri: str,
    template_sample: str,
    append: bool = False,
    extents: Optional[Tuple[float, float, float, float, float, float]] = None,
    offsets: Optional[Tuple[float, float, float, float, float, float]] = None,
    scales: Optional[Tuple[float, float, float, float, float, float]] = None,
    chunk_size: Optional[int] = POINT_CLOUD_CHUNK_SIZE,
    verbose: bool = False,
    config: Optional[Mapping[str, Any]] = None,
    id: str = "pointcloud",
    trace: bool = False,
    log_uri: Optional[str] = None,
):
    """Internal udf that ingests server side batch of point cloud files
    into tiledb arrays using PDAL API. Compression uses the default profile
    built in to PDAL.

    :param sources: Sequence of input point cloud file names
    :param dataset_uri: str, output TileDB array name
    :param template_sample: first point cloud to be ingested to initialize the array
    :param append: bool, whether to append to the array
    :param extents: Tuple, extents of point cloud, minx,maxx,miny,maxy,minz,maxz
    :param scales: Tuple, scale values for point cloud, ordered as x,y,z
    :param offsets: Tuple, offset values for point cloud, ordered as x,y,z
    :param chunk_size: PDAL configuration for chunking fragments
    :param verbose: verbose logging, defaults to False
    :param config: dict, configuration to pass on tiledb.VFS
    :param id: str, ID for logging, defaults to None
    :param trace, bool, enable trace logging
    :param log_uri: log array URI
    """
    import laspy
    import pdal

    import tiledb

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            vfs = tiledb.VFS()
            logger = get_logger_wrapper(verbose)

            def scale_array(arr):
                for idx, d in enumerate(["X", "Y", "Z"]):
                    arr[d] = offsets[idx] + (arr[d] * scales[idx])
                return arr

            if append:
                for f in sources:
                    logger.debug("ingesting point cloud %r", f)
                    with vfs.open(f, "rb") as src:
                        las = laspy.open(src)
                        chunk_itr = las.chunk_iterator(chunk_size)

                        for chunk in chunk_itr:
                            arr = scale_array(chunk.array)
                            pipeline = pdal.Writer.tiledb(
                                array_name=dataset_uri, append=append
                            ).pipeline(arr)
                            pipeline.execute()
            else:
                if extents and offsets and scales and template_sample:
                    logger.debug("creating point cloud schema from %r", template_sample)
                    with vfs.open(template_sample, "rb") as src:
                        las = laspy.open(src)
                        chunk_itr = las.chunk_iterator(chunk_size)
                        first_chunk = next(chunk_itr)
                        arr = scale_array(first_chunk.array)

                        pipeline = pdal.Writer.tiledb(
                            array_name=dataset_uri,
                            x_domain_st=extents.minx - 1,
                            y_domain_st=extents.miny - 1,
                            z_domain_st=extents.minz - 1,
                            x_domain_end=extents.maxx + 1,
                            y_domain_end=extents.maxy + 1,
                            z_domain_end=extents.maxz + 1,
                            offset_x=offsets[0],
                            offset_y=offsets[1],
                            offset_z=offsets[1],
                            scale_x=scales[0],
                            scale_y=scales[1],
                            scale_z=scales[1],
                            chunk_size=chunk_size,
                        ).pipeline(arr)
                        pipeline.execute()

                        for chunk in chunk_itr:
                            arr = scale_array(chunk.array)
                            pipeline = pdal.Writer.tiledb(
                                array_name=dataset_uri, append=True
                            ).pipeline(arr)
                            pipeline.execute()
                else:
                    raise ValueError("Insufficient metadata for point cloud ingestion")

            logger.info("max memory usage: %.3f GiB", max_memory_usage() / (1 << 30))


def ingest_raster_udf(
    input_blocks: Optional[Tuple[GeoBlockMetadata, ...]] = None,
    *,
    dataset_uri: str,
    extents: Optional[BoundingBox] = None,
    band_count: Optional[int] = None,
    dtype: Optional[str] = None,
    res: Optional[Tuple[float, float]] = None,
    crs: Optional[str] = None,
    nodata: Optional[float] = None,
    tile_size: int = RASTER_TILE_SIZE,
    resampling: str = "bilinear",
    append: bool = False,
    verbose: bool = False,
    config: Optional[Mapping[str, Any]] = None,
    compressor: Optional[dict] = None,
    id: str = "raster",
    trace: bool = False,
    log_uri: Optional[str] = None,
):
    """Internal udf that ingests server side batch of raster files
    into tiledb arrays using Rasterio API

    :param dataset_uri: str, output TileDB array name
    :param input_blocks: tuple, sequence of GeoBlockMetadata objects containing
        the destination raster window and the input files
        that contribute to this window
    :param extents: Extents of the destination raster
    :param band_count: int, number of bands in destination array
    :param dtype: str, dtype of destination array
    :param res: Tuple[float, float], resolution in x/y of the destination raster
    :param crs: str, CRS for the destination dataset
    :param nodata: float, NODATA value for destination raster
    :param resampling: string, resampling method,
        one of None, bilinear, cubic, nearest and average
    :param append: bool, whether to append to the array
    :param verbose: verbose logging, defaults to False
    :param config: dict, configuration to pass on tiledb.VFS
    :param compressor: dict, serialized compression filter
    :param id: str, ID for logging, defaults to None
    :param trace, bool, enable trace logging
    :param log_uri: log array URI
    """

    import rasterio
    import rasterio.merge

    import tiledb
    from tiledb.cloud.utilities import Profiler
    from tiledb.cloud.utilities import get_logger_wrapper
    from tiledb.cloud.utilities import max_memory_usage

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            vfs = tiledb.VFS()

            if not append:
                from rasterio.transform import from_origin

                from tiledb import filter

                if (
                    extents is None
                    or res is None
                    or crs is None
                    or band_count is None
                    or dtype is None
                ):
                    raise ValueError(
                        """CRS, band count, extents and resolution are
                        required to create empty raster array"""
                    )

                # create empty array,
                dst_profile = {
                    "count": band_count,
                    "dtype": dtype,
                    "driver": "TileDB",
                    "crs": crs,
                    "transform": from_origin(extents.minx, extents.maxy, *res),
                    "width": math.floor((extents.maxx - extents.minx) / res[0]),
                    "height": math.floor((extents.maxy - extents.miny) / res[1]),
                    "blockysize": tile_size,
                    "blockxsize": tile_size,
                }

                logger.debug("Destination raster profile %r", dst_profile)

                if nodata is not None:
                    dst_profile.update(
                        {
                            "nodata": nodata,
                        }
                    )

                if compressor:
                    compressor_args = dict(compressor)
                    compressor_name = compressor_args.pop("_name")
                    if compressor_name:
                        compressor_args = {
                            k: None if not v else v for k, v in compressor_args.items()
                        }
                        compression_filter = vars(filter).get(compressor_name)(
                            **compressor_args
                        )
                        compression_level = compression_filter.level

                    else:
                        raise ValueError

                    with rasterio.open(
                        dataset_uri,
                        mode="w",
                        COMPRESSION=compressor_name[
                            :-6
                        ].upper(),  # remove trailing `Filter`
                        COMPRESSION_LEVEL=compression_level,
                        **dst_profile,
                    ):
                        pass
                else:
                    with rasterio.open(
                        dataset_uri,
                        mode="w",
                        **dst_profile,
                    ):
                        pass

                logger.debug("Raster array created %r", dataset_uri)
            else:
                # srcs and dst have same number of bands
                if resampling:
                    resampling = rasterio.enums.Resampling[resampling.lower()]
                with rasterio.open(dataset_uri, mode="r+") as dst:
                    for blk in input_blocks:
                        input_datasets = [
                            rasterio.open(f, opener=vfs.open) for f in blk.files
                        ]
                        try:
                            row_off = blk.ranges[0][0]
                            col_off = blk.ranges[1][0]
                            dst_window = rasterio.windows.Window(
                                col_off,
                                row_off,
                                blk.ranges[1][1] - col_off,
                                blk.ranges[0][1] - row_off,
                            )
                            dst_bounds = rasterio.windows.bounds(
                                dst_window, dst.transform
                            )

                            for b in range(dst.count):
                                if len(input_datasets) == 1:
                                    # TODO deploy rasterio.merge update
                                    with rasterio.vrt.WarpedVRT(
                                        input_datasets[0],
                                        crs=dst.crs,
                                        transform=dst.transform,
                                        resampling=resampling,
                                        width=dst.width,
                                        height=dst.height,
                                        masked=True,
                                    ) as vrt:
                                        data = vrt.read(window=dst_window)
                                        dst.write(
                                            data[b], window=dst_window, indexes=b + 1
                                        )
                                else:
                                    data, _ = rasterio.merge.merge(
                                        input_datasets,
                                        bounds=dst_bounds,
                                        res=dst.res,
                                        nodata=dst.nodata,
                                        dtype=dst.profile["dtype"],
                                        resampling=resampling,
                                        indexes=[b + 1],
                                    )
                                    dst.write(data[0], window=dst_window, indexes=b + 1)
                        finally:
                            map(lambda s: s.close(), input_datasets)

            logger.info("max memory usage: %.3f GiB", max_memory_usage() / (1 << 30))


def read_uris(
    list_uri: str,
    dataset_type: DatasetType,
    *,
    log_uri: Optional[str] = None,
    config: Optional[Mapping[str, Any]] = None,
    max_files: Optional[int] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Read a list of URIs from a URI.

    :param list_uri: URI of the list of URIs
    :param dataset_type: dataset type, one of pointcloud, raster or geometry
    :param log_uri: log array URI
    :param config: config dictionary, defaults to None
    :param max_files: maximum number of URIs returned, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: list of URIs
    """

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri):
            result = []
            vfs = tiledb.VFS()
            for line in vfs.open(list_uri):
                result.append(line.decode().strip())
                if max_files and len(result) == max_files:
                    break

            logger.info(
                "Found %d %r geospatial datasets.", len(result), dataset_type.name
            )

        return result


def register_dataset_udf(
    dataset_uri: str,
    *,
    register_name: str,
    namespace: Optional[str] = None,
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> None:
    """
    Register the dataset on TileDB Cloud.

    :param dataset_uri: dataset URI
    :param register_name: name to register the dataset with on TileDB Cloud
    :param namespace: TileDB Cloud namespace, defaults to the user's default namespace
    :param config: config dictionary, defaults to None
    :param verbose: verbose logging, defaults to False
    """

    logger = get_logger_wrapper(verbose)

    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    tiledb_uri = f"tiledb://{namespace}/{register_name}"

    with tiledb.scope_ctx(config):
        found = False
        try:
            object_type = tiledb.object_type(tiledb_uri)
            if object_type == "group":
                found = True
            elif object_type is not None:
                raise ValueError(
                    f"Another object is already registered at '{tiledb_uri}'."
                )

        except Exception:
            # tiledb.object_type raises an exception if the namespace does not exist
            logger.error(
                "Error checking if %r is registered. Bad namespace?", tiledb_uri
            )
            raise

        if found:
            logger.info("Dataset already registered at %r.", tiledb_uri)
        else:
            logger.info("Registering dataset at %r.", tiledb_uri)
            tiledb.cloud.groups.register(
                dataset_uri,
                name=register_name,
                namespace=namespace,
            )


def ingest_datasets_dag(
    dataset_uri: str,
    *,
    dataset_type: DatasetType,
    acn: Optional[str] = None,
    config=None,
    namespace: Optional[str] = None,
    register_name: Optional[str] = None,
    search_uri: Optional[str] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    dataset_list_uri: Optional[str] = None,
    max_files: Optional[int] = None,
    compression_filter: Optional[dict] = None,
    workers: int = MAX_WORKERS,
    batch_size: int = BATCH_SIZE,
    tile_size: int = RASTER_TILE_SIZE,
    chunk_size: int = POINT_CLOUD_CHUNK_SIZE,
    nodata: Optional[float] = None,
    resampling: Optional[str] = "bilinear",
    res: Tuple[float, float] = None,
    verbose: bool = False,
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> None:
    """
    Ingests geospatial point clouds, geometries and images into TileDB arrays

    :param dataset_uri: dataset URI
    :param dataset_type: dataset type, one of pointcloud, raster or geometry
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param config: config dictionary, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param register_name: name to register the dataset with on TileDB Cloud,
        defaults to None
    :param search_uri: URI to search for geospatial dataset files, defaults to None
    :param pattern: Unix shell style pattern to match when searching for files,
        defaults to None
    :param ignore: Unix shell style pattern to ignore when searching for files,
        defaults to None
    :param dataset_list_uri: URI with a list of dataset URIs, defaults to None
    :param max_files: maximum number of URIs to read/find,
        defaults to None (no limit)
    :param compression_filter: serialized tiledb filter,
        defaults to None
    :param workers: number of workers for dataset ingestion, defaults to MAX_WORKERS
    :param batch_size: batch size for dataset ingestion, defaults to BATCH_SIZE
    :param tile_size: for rasters this is the tile (block) size
        for the merged destination array, defaults to 1024
    :param chunk_size: for point cloud this is the PDAL chunk size, defaults to 1000000
    :param nodata: NODATA value for raster merging
    :param resampling: string, resampling method,
        one of None, bilinear, cubic, nearest and average
    :param res: Tuple[float, float], output resolution in x/y
    :param verbose: verbose logging, defaults to False
    :param trace: bool, enabling log tracing, defaults to False
    :param log_uri: log array URI
    """

    logger = get_logger_wrapper(verbose)

    if log_uri:
        create_log_array(log_uri)

    kwargs = {}
    fn = None

    if dataset_list_uri:
        sources = read_uris(
            dataset_list_uri,
            dataset_type=dataset_type,
            log_uri=log_uri,
            config=config,
            max_files=max_files,
        )

    def pointcloud_match(f):
        return os.path.splitext(f)[-1].lstrip(".").lower() in ["las", "laz"]

    def raster_match(f):
        try:
            rasterio.driver_from_extension(f)
            return True
        except ValueError:
            return False

    def geometry_match(f):
        try:
            fiona.drvsupport.driver_from_extension(f)
            return True
        except ValueError:
            return False

    funcs = {
        DatasetType.POINTCLOUD: {
            "udf_fn": ingest_point_cloud_udf,
            "pattern_fn": pointcloud_match,
            "meta_fn": get_pointcloud_metadata,
        },
        DatasetType.RASTER: {
            "udf_fn": ingest_raster_udf,
            "pattern_fn": raster_match,
            "meta_fn": get_raster_metadata,
        },
        DatasetType.GEOMETRY: {
            "udf_fn": ingest_geometry_udf,
            "geometry_fn": geometry_match,
            "meta_fn": get_geometry_metadata,
        },
    }

    if search_uri:
        sources = find(
            search_uri,
            config=config,
            excludes=ignore,
            includes=pattern if pattern else funcs[dataset_type]["pattern_fn"],
            max_files=max_files,
        )

    if len(sources) == 0:
        raise ValueError(f"No {dataset_type.name} datasets found")

    meta = funcs[dataset_type]["meta_fn"](sources, config=config)
    if dataset_type == DatasetType.POINTCLOUD:
        if len(meta.paths) > 0:
            kwargs.update(
                {
                    "template_sample": meta.paths[0],
                    "extents": meta.extents,
                    "offsets": meta.offsets,
                    "scales": meta.scales,
                    "chunk_size": chunk_size,
                }
            )
            samples = meta.paths[1:]
        else:
            raise ValueError("Require at least one point cloud file to have been found")
    elif dataset_type == DatasetType.RASTER:
        kwargs.update(
            {
                "crs": meta.crs,
                "extents": meta.extents,
                "res": meta.res,
                "band_count": meta.band_count,
                "dtype": meta.dtype,
                "nodata": nodata,
                "resampling": resampling,
                "tile_size": tile_size,
                "compressor": compression_filter,
            }
        )
        samples = meta.block_metadata
    elif dataset_type == DatasetType.GEOMETRY:
        kwargs.update(
            {
                "extents": meta.extents,
            }
        )
    else:
        raise ValueError(f"Unsupported ingestion dataset type: {dataset_type.name}")

    fn = funcs[dataset_type]["udf_fn"]

    if os.environ.get("UNIT_TESTING"):
        # unit test inner functions
        # set up function
        fn(
            dataset_uri=dataset_uri,
            append=False,
            verbose=verbose,
            trace=trace,
            log_uri=log_uri,
            **kwargs,
        )
        # work functions
        for i, work in enumerate(batch(samples, batch_size)):
            fn(
                work,
                dataset_uri=dataset_uri,
                append=True,
                verbose=verbose,
                trace=trace,
                log_uri=log_uri,
                **kwargs,
            )
    else:
        # Build the task graph
        dag_name = f"{dataset_type.name}-{DEFAULT_DAG_NAME}"
        task_prefix = f"{dataset_type.name} - Task"

        logger.info("Building graph")
        graph = tiledb.cloud.dag.DAG(
            name=dag_name,
            mode=tiledb.cloud.dag.Mode.BATCH,
            max_workers=workers,
            namespace=namespace,
        )

        nodes = []

        # create first node
        ingest_node = graph.submit(
            fn,
            dataset_uri=dataset_uri,
            config=config,
            append=False,
            verbose=verbose,
            trace=trace,
            log_uri=log_uri,
            name=f"{task_prefix} - {0}",
            mode=tiledb.cloud.dag.Mode.BATCH,
            resources=DEFAULT_RESOURCES,
            image_name=DEFAULT_IMG_NAME,
            access_credentials_name=acn,
            **kwargs,
        )
        # work functions
        for i, work in enumerate(batch(samples, batch_size)):
            logger.info(f"Adding batch {i + 1}")
            n = graph.submit(
                fn,
                work,
                dataset_uri=dataset_uri,
                config=config,
                name=f"{task_prefix} - {i}",
                mode=tiledb.cloud.dag.Mode.BATCH,
                append=True,
                verbose=verbose,
                trace=trace,
                log_uri=log_uri,
                resources=DEFAULT_RESOURCES,
                image_name=DEFAULT_IMG_NAME,
                access_credentials_name=acn,
                **kwargs,
            )

            n.depends_on(ingest_node)
            nodes.append(n)

        graph.submit(
            consolidate_meta,
            dataset_uri,
            config,
            resources=DEFAULT_RESOURCES,
            verbose=verbose,
            log_uri=log_uri,
            access_credentials_name=acn,
        ).depends_on(nodes)

        # Register the dataset on TileDB Cloud
        if register_name:
            register_dataset_udf(
                dataset_uri,
                namespace=namespace,
                register_name=register_name,
                config=config,
                verbose=verbose,
                trace=trace,
                log_uri=log_uri,
                access_credentials_name=acn,
            )

        run_dag(graph, wait=False)

        logger.info(
            "%s geospatial datasets ingestion submitted -"
            " https://cloud.tiledb.com/activity/taskgraphs/%s/%s",
            dataset_type.name,
            graph.namespace,
            graph.server_graph_uuid,
        )


def consolidate_meta(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    id: str = "consolidate",
    verbose: bool = False,
    log_array_uri: Optional[str] = None,
) -> None:
    """
    Consolidate arrays in the dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param id: profiler event id, defaults to "consolidate"
    :param verbose: verbose logging, defaults to False
    """

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_array_uri, id=id):
            modes = ["commits", "fragment_meta", "array_meta"]

            for mode in modes:
                config = tiledb.Config({"sm.consolidation.mode": mode})
                try:
                    tiledb.consolidate(dataset_uri, config=config)
                except Exception as e:
                    print(e)

            for mode in modes:
                config = tiledb.Config({"sm.vacuum.mode": mode})
                try:
                    tiledb.vacuum(dataset_uri, config=config)
                except Exception as e:
                    print(e)

    logger.info("max memory usage: %.3f GiB", max_memory_usage() / (1 << 30))


def ingest_datasets(
    dataset_uri: str,
    *,
    dataset_type: DatasetType,
    acn: Optional[str] = None,
    config=None,
    namespace: Optional[str] = None,
    register_name: Optional[str] = None,
    search_uri: Optional[str] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    dataset_list_uri: Optional[str] = None,
    max_files: Optional[int] = None,
    compression_filter: Optional[dict] = None,
    workers: int = MAX_WORKERS,
    batch_size: int = BATCH_SIZE,
    tile_size: int = RASTER_TILE_SIZE,
    chunk_size: int = POINT_CLOUD_CHUNK_SIZE,
    nodata: Optional[float] = None,
    res: Tuple[float, float] = None,
    verbose: bool = False,
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> None:
    """
    Ingest samples into a dataset.

    :param dataset_uri: dataset URI
    :param dataset_type: dataset type, one of pointcloud, raster or geometry
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param config: config dictionary, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param register_name: name to register the dataset with on TileDB Cloud,
        defaults to None
    :param search_uri: URI to search for geospatial dataset files, defaults to None
    :param pattern: Unix shell style pattern to match when searching for files,
        defaults to None
    :param ignore: Unix shell style pattern to ignore when searching for files,
        defaults to None
    :param dataset_list_uri: URI with a list of dataset URIs, defaults to None
    :param max_files: maximum number of URIs to read/find,
        defaults to None (no limit)
    :param max_samples: maximum number of samples to ingest, defaults to None (no limit)
    :param compression_filter: serialized tiledb filter,
        defaults to None
    :param workers: number of workers for dataset ingestion, defaults to MAX_WORKERS
    :param batch_size: batch size for dataset ingestion, defaults to BATCH_SIZE
    :param tile_size: for rasters this is the tile (block) size
        for the merged destination array defaults to 1024
    :param chunk_size: for point cloud this is the PDAL chunk size, defaults to 1000000
    :param nodata: NODATA value for rasters
    :param res: Tuple[float, float], output resolution in x/y
    :param verbose: verbose logging, defaults to False
    :param trace: bool, enable trace for logging, defaults to False
    :param log_uri: log array URI
    """

    # Validate user input
    if bool(search_uri) & bool(dataset_list_uri):
        raise ValueError(
            "Exactly one of `search_uri` or `dataset_list_uri` must be provided."
        )

    if not search_uri and (pattern or ignore):
        raise ValueError("Only specify `pattern` or `ignore` with `search_uri`.")

    # Remove any trailing slashes
    dataset_uri = dataset_uri.rstrip("/")

    logger = get_logger_wrapper(verbose)
    logger.info("Ingesting datasets into %r", dataset_uri)

    # Ingest datasets
    ingest_datasets_dag(
        dataset_uri,
        dataset_type=dataset_type,
        acn=acn,
        config=config,
        namespace=namespace,
        register_name=register_name,
        search_uri=search_uri,
        pattern=pattern,
        ignore=ignore,
        dataset_list_uri=dataset_list_uri,
        max_files=max_files,
        compression_filter=compression_filter,
        workers=workers,
        batch_size=batch_size,
        tile_size=tile_size,
        chunk_size=chunk_size,
        nodata=nodata,
        res=res,
        verbose=verbose,
        trace=trace,
        log_uri=log_uri,
    )


# Wrapper function for batch dataset ingestion
ingest = as_batch(ingest_datasets)
