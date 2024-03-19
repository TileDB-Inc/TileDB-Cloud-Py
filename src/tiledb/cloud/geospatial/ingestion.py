import logging
import math
import os
from enum import Enum
from fnmatch import fnmatch
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

import attrs
import fiona
import laspy
import rasterio
import shapely
from rtree import index

import tiledb
from tiledb.cloud.utilities import Profiler
from tiledb.cloud.utilities import as_batch

# from tiledb.cloud.utilities import chunk
from tiledb.cloud.utilities import create_log_array
from tiledb.cloud.utilities import get_logger  # get_logger_wrapper
from tiledb.cloud.utilities import max_memory_usage
from tiledb.cloud.utilities import run_dag

T = TypeVar("T")


def chunk(items: Sequence[T], chunk_size: int) -> Iterator[Sequence[T]]:
    """Chunks a sequence of objects and returns an iterator where
    each return sequence is of length chunk_size.

    :param items: Sequence to split into batches
    :param chunk_size: Size of chunks of the sequence to return
    """
    # Iterator for providing batches of chunks
    length = len(items)
    for ndx in range(0, length, chunk_size):
        yield items[ndx : min(ndx + chunk_size, length)]


def get_logger_wrapper(
    verbose: bool = False,
) -> logging.Logger:
    """
    Get a logger instance and log version information.

    :param verbose: verbose logging, defaults to False
    :return: logger instance
    """

    level = logging.DEBUG if verbose else logging.INFO
    logger = get_logger(level)

    logger.debug(
        "tiledb.cloud=%s, tiledb=%s, libtiledb=%s",
        tiledb.cloud.__version__,
        tiledb.version(),
        tiledb.libtiledb.version(),
    )

    return logger


def find(
    uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    include: Optional[Union[str, Callable]] = None,
    exclude: Optional[Union[str, Callable]] = None,
    max_count: Optional[int] = None,
) -> Iterator[str]:
    """Searches a path for files matching the include/exclude pattern using VFS.

    :param uri: Input path to search
    :param config: Optional dict configuration to pass on tiledb.VFS
    :param include: Optional include pattern string
    :param exclude: Optional exclude pattern string
    :param max_count: Optional stop point when searching for files
    """
    with tiledb.scope_ctx(config):
        vfs = tiledb.VFS(config=config, ctx=tiledb.Ctx(config))
        listing = vfs.ls(uri)
        current_count = 0

        def list_files(listing):
            for f in listing:
                # Avoid infinite recursion
                if f == uri:
                    continue

                if vfs.is_dir(f):
                    yield from list_files(
                        vfs.ls(f),
                    )
                else:
                    # Skip files that do not match the include pattern or match
                    # the exclude pattern.
                    if callable(include):
                        if not include(f):
                            continue
                    else:
                        if include and not fnmatch(f, include):
                            continue

                    if callable(exclude):
                        if exclude(f):
                            continue
                    else:
                        if exclude and fnmatch(f, exclude):
                            continue
                    yield f

        for f in list_files(listing):
            yield f

            current_count += 1
            if max_count and current_count == max_count:
                return


fiona.drvsupport.supported_drivers["TileDB"] = "arw"
fiona.vfs.SCHEMES["tiledb"] = "tiledb"

DEFAULT_RESOURCES = {"cpu": "2", "memory": "2Gi"}
DEFAULT_IMG_NAME = "3.9-geo"
DEFAULT_DAG_NAME = "geo-ingestion"

# Default values for ingestion parameters
RASTER_TILE_SIZE = 1024
PIXELS_PER_FRAGMENT = (RASTER_TILE_SIZE**2) * 10
POINT_CLOUD_CHUNK_SIZE = 1_000_000
GEOMETRY_CHUNK_SIZE = 100_000
MAX_WORKERS = 40
BATCH_SIZE = 10

XYZBoundsTuple = Tuple[float, float, float, float, float, float]
XYBoundsTuple = Tuple[float, float, float, float]
XYZTuple = Tuple[float, float, float]


class DatasetType(Enum):
    POINTCLOUD = 1
    RASTER = 2
    GEOMETRY = 3


@attrs.define
class BoundingBox:
    minx: float
    miny: float
    maxx: float
    maxy: float
    minz: Optional[float] = None
    maxz: Optional[float] = None

    @property
    def bounds(self) -> Union[XYBoundsTuple, XYZBoundsTuple]:
        if self.minz:
            return (self.minx, self.miny, self.minz, self.maxx, self.maxy, self.maxz)
        else:
            return (self.minx, self.miny, self.maxx, self.maxy)


@attrs.define
class GeoBlockMetadata:
    ranges: Tuple[Tuple[int, int], Tuple[int, int]]
    files: Tuple[os.PathLike, ...] = attrs.field(converter=tuple)


def _wrap_paths(
    paths: Optional[Union[Sequence[os.PathLike], os.PathLike]]
) -> Optional[Tuple[os.PathLike, ...]]:
    if paths is None:
        return None
        # Would it make sense to return () here, so it's always a Tuple[PathLike, ...]?
    if isinstance(paths, (str, bytes)) or not isinstance(paths, Sequence):
        # Editor's note: the isinstance has to go after the str-or-bytes check
        # because str and bytes are both Sequences.
        # (Worse yet, str is a Sequence[str].)
        return (paths,)
    return tuple(paths)


@attrs.define
class GeoMetadata:
    # common properties
    extents: BoundingBox
    crs: str = None
    paths: attrs.field(converter=_wrap_paths, default=None) = None
    # raster properties
    dtype: Optional[str] = None
    band_count: Optional[int] = None
    res: Optional[Tuple[float, float]] = None
    block_metadata: Optional[Tuple[GeoBlockMetadata, ...]] = None
    # point cloud properties
    scales: Optional[XYZTuple] = None
    offsets: Optional[XYZTuple] = None
    # geometry properties
    geometry_schema: Optional[dict] = None


def load_pointcloud_metadata(
    sources: Iterable[os.PathLike],
    *,
    config: Optional[Mapping[str, object]] = None,
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
    if not sources:
        raise ValueError("Input point cloud datasets required")

    def _fold_in(oper, existing, new):
        if existing is None:
            return new
        return [oper(e) for e in zip(existing, new)]

    with tiledb.scope_ctx(config):
        vfs = tiledb.VFS()
        logger = get_logger_wrapper(verbose)
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            offsets = None
            scales = None
            mins = None
            maxs = None
            paths = list(sources)
            for f in paths:
                logger.debug("finding metadata for %r", f)
                with vfs.open(f, "rb") as src:
                    # only open header
                    las = laspy.open(src)
                    hdr = las.header
                    mins = _fold_in(min, mins, hdr.mins)
                    maxs = _fold_in(max, maxs, hdr.maxs)
                    scales = _fold_in(max, scales, hdr.scales)
                    offsets = _fold_in(min, offsets, hdr.offsets)

            return GeoMetadata(
                paths=paths,
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


def load_geometry_metadata(
    sources: Iterable[os.PathLike],
    *,
    config: Optional[Mapping[str, object]] = None,
    verbose: bool = False,
    id: str = "pointcloud_metadata",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> GeoMetadata:
    """Return geospatial metadata for a sequence of input geometry data files

    :param sources: A sequence of paths or path to input
    :param config: dict configuration to pass on tiledb.VFS
    :param verbose: bool, enable verbose logging, default is False
    :param trace: bool, enable trace logging, default is False
    :param log_uri: Optional[str] = None,
    :Return: GeoMetadata, a populated GeoMetadata object
    """
    # note this will be refactored to use /vsipyopener in fiona
    if not sources:
        raise ValueError("Input point cloud datasets required")

    with tiledb.scope_ctx(config):
        tiledb.VFS()
        logger = get_logger_wrapper(verbose)
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            # for geometries we need the maximum extents
            # and to check geometry types / crs are the same
            schema = None
            full_extents = None
            crs = None

            for pth in sources:
                logger.debug("finding metadata for %r", pth)
                with fiona.open(pth) as src:
                    crs = src.crs if crs is None else crs
                    if src.crs != crs:
                        raise ValueError("All datasets need to be in the same CRS")

                    schema = src.schema if schema is None else schema
                    if src.schema != schema:
                        raise ValueError("All datasets need to have the same schema")

                    # 2.5 is supported internally but not needed for ingest
                    extents = BoundingBox(
                        minx=src.bounds[0],
                        miny=src.bounds[1],
                        maxx=src.bounds[2],
                        maxy=src.bounds[3],
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

            return GeoMetadata(
                extents=full_extents, crs=crs, paths=sources, geometry_schema=schema
            )


def load_raster_metadata(
    sources: Iterable[os.PathLike],
    *,
    config: Optional[Mapping[str, object]] = None,
    pixels_per_fragment: int = PIXELS_PER_FRAGMENT,
    res: Tuple[float, float] = None,
    verbose: bool = False,
    id: str = "raster_metadata",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> GeoMetadata:
    """Return geospatial metadata for a sequence of input raster data files

    :param sources: iterator, paths or path to process
    :param config: dict, configuration to pass on tiledb.VFS
    :param pixels_per_fragment: for rasters this this the number of tiles
        that will be processed together per fragment. Ideally aim to align
        as a factor of tile_size
    :param verbose: bool, enable verbose logging, default is False
    :param trace: bool, enable trace logging, default is False
    :param log_uri: Optional[str] = None,
    :Return: GeoMetadata, a populated GeoMetadata objects with blocks
             and the files that contribute to each block
    """
    if not sources:
        raise ValueError("Input raster datasets required")

    logger = get_logger_wrapper(verbose)
    full_extents = None
    crs = None
    num_bands = None
    dtype = None

    if res:
        xres, yres = res
        do_res_check = False
    else:
        do_res_check = True
        xres = None
        yres = None

    def group_by_raster_block(
        meta: Sequence[GeoMetadata],
    ) -> Tuple[GeoBlockMetadata, ...]:
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

        dst_transform = rasterio.transform.from_bounds(
            *full_extents.bounds, width, height
        )

        dst_windows = rasterio.windows.window_split(height, width, pixels_per_fragment)

        results = []
        for _, w in dst_windows:
            region_bounds = rasterio.windows.bounds(w, dst_transform)
            # find intersection
            intersects = tuple(idx.intersection(region_bounds))
            if intersects:
                # append the result in pixel coords
                results.append(
                    GeoBlockMetadata(
                        ranges=w.toranges(),
                        files=[meta[s].paths for s in intersects],
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
                    crs = src.crs if crs is None else crs
                    if crs != src.crs:
                        raise ValueError("All datasets need to be in the same CRS")

                    num_bands = src.count if num_bands is None else num_bands
                    if num_bands != src.count:
                        raise ValueError(
                            "All datasets need to have the same number of bands"
                        )

                    dtype = src.profile["dtype"] if dtype is None else dtype

                    if dtype != src.profile["dtype"]:
                        raise ValueError("All datasets need to have the same data type")

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
    *,
    dataset_uri: str,
    args: Union[Dict, List] = {},
    sources: Sequence[str] = None,
    schema: dict = None,
    extents: Optional[XYBoundsTuple] = None,
    crs: Optional[str] = None,
    chunk_size: Optional[int] = GEOMETRY_CHUNK_SIZE,
    batch_size: Optional[int] = BATCH_SIZE,
    compressor: Optional[dict] = None,
    append: bool = False,
    verbose: bool = False,
    stats: bool = False,
    config: Optional[Mapping[str, object]] = None,
    id: str = "geometry",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> Union[Sequence[os.PathLike], None]:
    """Internal udf that ingests server side batch of geometry files
    into tiledb arrays using Fiona API

    :param dataset_uri: str, output TileDB array name
    :param args: dict, input key value arguments as a dictionary
    :param sources: Sequence of input geometry file names
    :param schema: dict, dictionary of schema attributes and geometries
    :param extents: Extents of the destination geometry array
    :param crs: str, CRS for the destination dataset
    :param chunk_size: int, sets tile capacity and
                       the number of geometries written at once
    :param batch_size: batch size for dataset ingestion, defaults to BATCH_SIZE
    :param compressor: dict, serialized compression filter
    :param append: bool, whether to append to the array
    :param verbose: verbose logging, defaults to False
    :param stats: bool, print TileDB stats to stdout
    :param config: dict, configuration to pass on tiledb.VFS
    :param id: str, ID for logging, defaults to None
    :param trace, bool, enable trace logging
    :param log_uri: log array URI
    :return: if not appending then the function returns a tuple of file paths
    """
    import fiona

    from tiledb import filter

    if sources is None and "sources" in args:
        sources = args["sources"]

    if not append:
        if schema is None and "schema" in args:
            schema = args["schema"]
        if extents is None and "extents" in args:
            extents = args["extents"]
        if crs is None and "crs" in args:
            crs = args["crs"]
        if chunk_size is None and "chunk_size" in args:
            chunk_size = args["chunk_size"]
        if compressor is None and "compressor" in args:
            compressor = args["compressor"]

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            tiledb.VFS()
            logger = get_logger_wrapper(verbose)
            try:
                if append:
                    for f in sources:
                        logger.debug("ingesting geometry dataset %r", f)
                        with fiona.open(f) as colxn:
                            with fiona.open(
                                dataset_uri, mode="a", STATS=stats, driver="TileDB"
                            ) as dst:
                                for feat in colxn:
                                    # TileDB OGR buffer features internally
                                    # so we can write one at a time
                                    dst.write(feat)
                    return

                if extents and crs:
                    logger.debug("creating geometry schema for %r", dataset_uri)
                    if compressor:
                        compressor_args = dict(compressor)
                        compressor_type = compressor_args.pop("_type")
                        if compressor_type:
                            compression_filter = getattr(filter, compressor_type)(
                                **{k: v or None for k, v in compressor_args.items()}
                            )
                            compression_level = compression_filter.level
                        else:
                            raise ValueError("Compression filter name not specified")

                        # remove trailing `Filter`
                        compressor_type = compressor_type[:-6].upper()

                        with fiona.open(
                            dataset_uri,
                            driver="TileDB",
                            schema=schema,
                            crs=crs,
                            BATCH_SIZE=chunk_size,
                            TILE_CAPACITY=chunk_size,
                            COMPRESSION=compressor_type,
                            COMPRESSION_LEVEL=compression_level,
                            STATS=stats,
                            BOUNDS=",".join(str(v) for v in extents),
                        ):
                            pass
                    else:
                        with fiona.open(
                            dataset_uri,
                            mode="w",
                            driver="TileDB",
                            schema=schema,
                            crs=crs,
                            BATCH_SIZE=chunk_size,
                            TILE_CAPACITY=chunk_size,
                            STATS=stats,
                            BOUNDS=",".join(str(v) for v in extents),
                        ) as dst:
                            pass

                    return list(chunk(sources, batch_size))
                else:
                    raise ValueError("Insufficient metadata for geometry ingestion")
            finally:
                logger.info(
                    "max memory usage: %.3f GiB", max_memory_usage() / (1 << 30)
                )


def ingest_point_cloud_udf(
    *,
    args: Union[Dict, List] = {},
    dataset_uri: str,
    sources: Sequence[str] = None,
    template_sample: str = None,
    append: bool = False,
    extents: Optional[XYZBoundsTuple] = None,
    offsets: Optional[XYZTuple] = None,
    scales: Optional[XYZTuple] = None,
    chunk_size: Optional[int] = POINT_CLOUD_CHUNK_SIZE,
    batch_size: Optional[int] = BATCH_SIZE,
    verbose: bool = False,
    stats: bool = False,
    config: Optional[Mapping[str, object]] = None,
    id: str = "pointcloud",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> Union[Sequence[os.PathLike], None]:
    """Internal udf that ingests server side batch of point cloud files
    into tiledb arrays using PDAL API. Compression uses the default profile
    built in to PDAL.

    :param args: dict, input key value arguments as a dictionary
    :param dataset_uri: str, output TileDB array name
    :param sources: Sequence of input point cloud file names
    :param template_sample: first point cloud to be ingested to initialize the array
    :param append: bool, whether to append to the array
    :param extents: Tuple, extents of point cloud, minx,maxx,miny,maxy,minz,maxz
    :param scales: Tuple, scale values for point cloud, ordered as x,y,z
    :param offsets: Tuple, offset values for point cloud, ordered as x,y,z
    :param chunk_size: PDAL configuration for chunking fragments
    :param batch_size: batch size for dataset ingestion, defaults to BATCH_SIZE
    :param verbose: verbose logging, defaults to False
    :param stats: bool, print TileDB stats to stdout
    :param config: dict, configuration to pass on tiledb.VFS
    :param id: str, ID for logging, defaults to None
    :param trace, bool, enable trace logging
    :param log_uri: log array URI
    :return: if not appending then a sequence of file paths
    """
    import laspy
    import numpy as np
    import pdal

    import tiledb

    if sources is None and "sources" in args:
        sources = args["sources"]
    if chunk_size is None and "chunk_size" in args:
        chunk_size = args["chunk_size"]

    if not append:
        if template_sample is None and "template_sample" in args:
            template_sample = args["template_sample"]
        if extents is None and "extents" in args:
            extents = args["extents"]
        if offsets is None and "offsets" in args:
            offsets = args["offsets"]
        if scales is None and "scales" in args:
            scales = args["scales"]

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            vfs = tiledb.VFS()
            logger = get_logger_wrapper(verbose)

            def get_pc_array(chunk):
                new_dt = np.dtype(
                    [("X", "float64"), ("Y", "float64"), ("Z", "float64")]
                    + chunk.array.dtype.descr[3:]
                )
                arr = np.array(chunk.array, dtype=new_dt)
                arr["X"] = chunk.x
                arr["Y"] = chunk.y
                arr["Z"] = chunk.z
                return arr

            try:
                if append:
                    for f in sources:
                        logger.debug("ingesting point cloud %r", f)
                        with vfs.open(f, "rb") as src:
                            las = laspy.open(src)
                            chunk_itr = las.chunk_iterator(chunk_size)

                            for c in chunk_itr:
                                arr = get_pc_array(c)
                                pipeline = pdal.Writer.tiledb(
                                    array_name=dataset_uri, stats=stats, append=append
                                ).pipeline(arr)
                                pipeline.execute()
                    return

                if extents and offsets and scales and template_sample:
                    logger.debug("creating point cloud schema from %r", template_sample)
                    with vfs.open(template_sample, "rb") as src:
                        las = laspy.open(src)
                        chunk_itr = las.chunk_iterator(chunk_size)
                        first_chunk = next(chunk_itr)
                        arr = get_pc_array(first_chunk)

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
                            offset_z=offsets[2],
                            scale_x=scales[0],
                            scale_y=scales[1],
                            scale_z=scales[2],
                            chunk_size=chunk_size,
                        ).pipeline(arr)
                        pipeline.execute()

                        for c in chunk_itr:
                            arr = get_pc_array(c)
                            pipeline = pdal.Writer.tiledb(
                                array_name=dataset_uri, stats=stats, append=True
                            ).pipeline(arr)
                            pipeline.execute()

                    return list(chunk(sources, batch_size))
                else:
                    raise ValueError("Insufficient metadata for point cloud ingestion")
            finally:
                logger.info(
                    "max memory usage: %.3f GiB", max_memory_usage() / (1 << 30)
                )


def ingest_raster_udf(
    *,
    args: Union[Dict, List] = {},
    dataset_uri: str,
    sources: Tuple[GeoBlockMetadata] = None,
    extents: Optional[BoundingBox] = None,
    band_count: Optional[int] = None,
    dtype: Optional[str] = None,
    res: Optional[Tuple[float, float]] = None,
    crs: Optional[str] = None,
    nodata: Optional[float] = None,
    tile_size: int = RASTER_TILE_SIZE,
    resampling: str = "bilinear",
    append: bool = False,
    batch_size: int = BATCH_SIZE,
    stats: bool = False,
    verbose: bool = False,
    config: Optional[Mapping[str, object]] = None,
    compressor: Optional[dict] = None,
    id: str = "raster",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> Union[Sequence[GeoBlockMetadata], None]:
    """Internal udf that ingests server side batch of raster files
    into tiledb arrays using Rasterio API

    :param args: dict, input key value arguments as a dictionary
    :param dataset_uri: str, output TileDB array name
    :param sources: tuple, sequence of GeoBlockMetadata objects containing
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
    :param batch_size: batch size for dataset ingestion, defaults to BATCH_SIZE
    :param stats: bool, print TileDB stats to stdout
    :param verbose: verbose logging, defaults to False
    :param config: dict, configuration to pass on tiledb.VFS
    :param compressor: dict, serialized compression filter
    :param id: str, ID for logging, defaults to None
    :param trace, bool, enable trace logging
    :param log_uri: log array URI
    :return: if not appending then a sequence of populated GeoBlockMetadata objects
    """

    import rasterio
    import rasterio.merge

    import tiledb
    from tiledb.cloud.utilities import Profiler

    # from tiledb.cloud.utilities import get_logger_wrapper
    from tiledb.cloud.utilities import max_memory_usage

    logger = get_logger_wrapper(verbose)

    if sources is None and "sources" in args:
        sources = args["sources"]
    if resampling is None and "resampling" in args:
        resampling = args["resampling"]

    if not append:
        if extents is None and "extents" in args:
            extents = args["extents"]
        if band_count is None and "band_count" in args:
            band_count = args["band_count"]
        if res is None and "res" in args:
            res = args["res"]
        if crs is None and "crs" in args:
            crs = args["crs"]
        if nodata is None and "nodata" in args:
            nodata = args["nodata"]
        if dtype is None and "dtype" in args:
            dtype = args["dtype"]
        if tile_size is None and "tile_size" in args:
            tile_size = args["tile_size"]
        if batch_size is None and "batch_size" in args:
            batch_size = args["batch_size"]
        if compressor is None and "compressor" in args:
            compressor = args["compressor"]

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            vfs = tiledb.VFS()
            try:
                if not append:
                    import rasterio
                    from rasterio.transform import from_origin

                    from tiledb import filter

                    if None in (
                        extents,
                        res,
                        crs,
                        band_count,
                        dtype,
                    ):
                        raise ValueError(
                            "CRS, band count, extents and resolution are"
                            "required to create empty raster array"
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
                        dst_profile.update(nodata=nodata)

                    if compressor:
                        compressor_args = dict(compressor)
                        compressor_type = compressor_args.pop("_type")
                        if compressor_type:
                            compression_filter = getattr(filter, compressor_type)(
                                **{k: v or None for k, v in compressor_args.items()}
                            )
                            compression_level = compression_filter.level
                        else:
                            raise ValueError("Compression filter name not specified")

                        # remove trailing `Filter`
                        compressor_type = compressor_type[:-6].upper()

                        with rasterio.open(
                            dataset_uri,
                            mode="w",
                            COMPRESSION=compressor_type,
                            COMPRESSION_LEVEL=compression_level,
                            STATS=stats,
                            **dst_profile,
                        ):
                            pass
                    else:
                        with rasterio.open(
                            dataset_uri,
                            mode="w",
                            STATS=stats,
                            **dst_profile,
                        ):
                            pass

                    logger.debug("Raster array created %r", dataset_uri)
                    return list(chunk(sources, batch_size))

                # srcs and dst have same number of bands
                if resampling:
                    resampling = rasterio.enums.Resampling[resampling.lower()]
                with rasterio.open(dataset_uri, mode="r+", driver="TileDB") as dst:
                    for c in sources:
                        input_datasets = [
                            rasterio.open(f, opener=vfs.open, STATS=stats)
                            for f in c.files
                        ]
                        try:
                            col_off = c.ranges[1][0]
                            row_off = c.ranges[0][0]
                            chunk_window = rasterio.windows.Window(
                                col_off,
                                row_off,
                                c.ranges[1][1] - col_off,
                                c.ranges[0][1] - row_off,
                            )
                            chunk_bounds = rasterio.windows.bounds(
                                chunk_window, dst.transform
                            )

                            for b in range(dst.count):
                                chunk_arr, _ = rasterio.merge.merge(
                                    input_datasets,
                                    bounds=chunk_bounds,
                                    nodata=nodata,
                                    indexes=[b + 1],
                                )
                                dst.write(chunk_arr, window=chunk_window)
                            logger.debug(
                                "Written %r bounds to %r", chunk_bounds, dataset_uri
                            )
                        finally:
                            for s in input_datasets:
                                s.close()
                return
            finally:
                logger.info(
                    "max memory usage: %.3f GiB", max_memory_usage() / (1 << 30)
                )


def read_uris(
    list_uri: str,
    dataset_type: DatasetType,
    *,
    log_uri: Optional[str] = None,
    config: Optional[Mapping[str, object]] = None,
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
    acn: Optional[str] = None,
    config: Optional[Mapping[str, object]] = None,
    verbose: bool = False,
) -> None:
    """
    Register the dataset on TileDB Cloud.

    :param dataset_uri: dataset URI
    :param register_name: name to register the dataset with on TileDB Cloud
    :param namespace: TileDB Cloud namespace, defaults to the user's default namespace
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param config: config dictionary, defaults to None
    :param verbose: verbose logging, defaults to False
    """

    import tiledb

    # from tiledb.cloud.utilities import get_logger_wrapper

    logger = get_logger_wrapper(verbose)

    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    tiledb_uri = f"tiledb://{namespace}/{register_name}"

    with tiledb.scope_ctx(config):
        found = False
        try:
            object_type = tiledb.object_type(tiledb_uri)
            if object_type == "array":
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
            tiledb.cloud.array.register_array(
                dataset_uri,
                array_name=register_name,
                namespace=namespace,
                access_credentials_name=acn,
            )


def build_inputs_udf(
    *,
    dataset_type: DatasetType,
    config: Optional[Mapping[str, object]] = None,
    search_uri: Optional[str] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    dataset_list_uri: Optional[str] = None,
    max_files: Optional[int] = None,
    compression_filter: Optional[dict] = None,
    tile_size: int = RASTER_TILE_SIZE,
    pixels_per_fragment: int = PIXELS_PER_FRAGMENT,
    chunk_size: int = POINT_CLOUD_CHUNK_SIZE,
    nodata: Optional[float] = None,
    resampling: Optional[str] = "bilinear",
    res: Tuple[float, float] = None,
    verbose: bool = False,
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> dict[str, object]:
    """Groups input URIs into batches.
    :param dataset_type: dataset type, one of pointcloud, raster or geometry
    :param config: config dictionary, defaults to None
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
    :param tile_size: for rasters this is the tile (block) size
        for the merged destination array, defaults to 1024
    :param pixels_per_fragment: for rasters this this the number of tiles
        that will be processed together per fragment. Ideally aim to align
        as a factor of tile_size
    :param chunk_size: for point cloud this is the PDAL chunk size, defaults to 1000000
    :param nodata: NODATA value for raster merging
    :param resampling: string, resampling method,
        one of None, bilinear, cubic, nearest and average
    :param res: Tuple[float, float], output resolution in x/y
    :param verbose: verbose logging, defaults to False
    :param trace: bool, enabling log tracing, defaults to False
    :param log_uri: log array URI
    :return: A dict containing the kwargs needed for the next function call
    """
    from tiledb.cloud.utilities import Profiler

    # from tiledb.cloud.utilities import find
    # from tiledb.cloud.utilities import get_logger_wrapper
    from tiledb.cloud.utilities import max_memory_usage

    logger = get_logger_wrapper(verbose)
    with Profiler(array_uri=log_uri, id=id, trace=trace):
        try:

            def raster_match(f: str):
                import rasterio

                try:
                    rasterio.driver_from_extension(f)
                    return True
                except ValueError:
                    return False

            def pointcloud_match(f: str):
                return os.path.splitext(f)[-1].lstrip(".").lower() in ["las", "laz"]

            def geometry_match(f: str):
                import fiona

                try:
                    fiona.drvsupport.driver_from_extension(f)
                    return True
                except ValueError:
                    return False

            fns = {
                DatasetType.POINTCLOUD: {
                    "pattern_fn": pointcloud_match,
                    "meta_fn": load_pointcloud_metadata,
                    "kwargs": {},
                },
                DatasetType.RASTER: {
                    "pattern_fn": raster_match,
                    "meta_fn": load_raster_metadata,
                    "kwargs": {
                        "pixels_per_fragment": pixels_per_fragment,
                        "res": res,
                    },
                },
                DatasetType.GEOMETRY: {
                    "pattern_fn": geometry_match,
                    "meta_fn": load_geometry_metadata,
                    "kwargs": {},
                },
            }

            kwargs = {}

            if dataset_list_uri:
                sources = read_uris(
                    dataset_list_uri,
                    dataset_type=dataset_type,
                    log_uri=log_uri,
                    config=config,
                    max_files=max_files,
                )

            if search_uri:
                sources = find(
                    search_uri,
                    config=config,
                    exclude=ignore,
                    include=pattern if pattern else fns[dataset_type]["pattern_fn"],
                    max_count=max_files,
                )

            if not sources:
                raise ValueError(f"No {dataset_type.name} datasets found")

            meta_kwargs = fns[dataset_type]["kwargs"]
            meta = fns[dataset_type]["meta_fn"](sources, config=config, **meta_kwargs)

            if dataset_type == DatasetType.POINTCLOUD:
                if len(meta.paths) == 0:
                    raise ValueError(
                        "Require at least one point cloud file to have been found"
                    )

                kwargs.update(
                    template_sample=meta.paths[0],
                    extents=meta.extents,
                    offsets=meta.offsets,
                    scales=meta.scales,
                    chunk_size=chunk_size,
                    sources=meta.paths[1:],
                )
            elif dataset_type == DatasetType.RASTER:
                kwargs.update(
                    crs=meta.crs,
                    extents=meta.extents,
                    res=res if res else meta.res,
                    band_count=meta.band_count,
                    dtype=meta.dtype,
                    nodata=nodata,
                    resampling=resampling,
                    tile_size=tile_size,
                    compressor=compression_filter,
                    sources=meta.block_metadata,
                )
            elif dataset_type == DatasetType.GEOMETRY:
                if len(meta.paths) > 0:
                    bounds = [
                        meta.extents.minx,
                        meta.extents.miny,
                        meta.extents.maxx,
                        meta.extents.maxy,
                    ]
                    kwargs.update(
                        extents=bounds,
                        chunk_size=chunk_size,
                        compressor=compression_filter,
                        crs=meta.crs,
                        schema=meta.geometry_schema,
                        sources=meta.paths,
                    )
                else:
                    raise ValueError(
                        "Require at least one geometry file to have been found"
                    )
            else:
                raise ValueError(
                    f"Unsupported ingestion dataset type: {dataset_type.name}"
                )

            return kwargs
        finally:
            logger.info("max memory usage: %.3f GiB", max_memory_usage() / (1 << 30))


def ingest_datasets_dag(
    dataset_uri: str,
    *,
    dataset_type: DatasetType,
    acn: Optional[str] = None,
    config: Optional[Mapping[str, object]] = None,
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
    pixels_per_fragment=PIXELS_PER_FRAGMENT,
    chunk_size: int = POINT_CLOUD_CHUNK_SIZE,
    nodata: Optional[float] = None,
    resampling: Optional[str] = "bilinear",
    res: Tuple[float, float] = None,
    stats: bool = False,
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
        defaults to None and the destination array is not registered
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
    :param pixels_per_fragment: for rasters this this the number of tiles
        that will be processed together per fragment. Ideally aim to align
        as a factor of tile_size
    :param chunk_size: for point cloud this is the PDAL chunk size, defaults to 1000000
    :param nodata: NODATA value for raster merging
    :param resampling: string, resampling method,
        one of None, bilinear, cubic, nearest and average
    :param res: Tuple[float, float], output resolution in x/y
    :param stats: bool, print TileDB stats to stdout
    :param verbose: verbose logging, defaults to False
    :param trace: bool, enabling log tracing, defaults to False
    :param log_uri: log array URI
    """

    logger = get_logger_wrapper(verbose)

    if log_uri:
        create_log_array(log_uri)

    funcs = {
        DatasetType.POINTCLOUD: {
            "udf_fn": ingest_point_cloud_udf,
        },
        DatasetType.RASTER: {
            "udf_fn": ingest_raster_udf,
        },
        DatasetType.GEOMETRY: {
            "udf_fn": ingest_geometry_udf,
        },
    }

    fn = funcs[dataset_type]["udf_fn"]

    # Build the task graph
    dag_name = f"{dataset_type.name.lower()}-{DEFAULT_DAG_NAME}"
    task_prefix = f"{dataset_type.name.lower()} - Task"

    logger.info("Building graph")
    graph = tiledb.cloud.dag.DAG(
        name=dag_name,
        mode=tiledb.cloud.dag.Mode.BATCH,
        max_workers=workers,
        namespace=namespace,
    )

    # find sources
    input_list_node = graph.submit(
        build_inputs_udf,
        dataset_type=dataset_type,
        access_credentials_name=acn,
        config=config,
        search_uri=search_uri,
        pattern=pattern,
        ignore=ignore,
        dataset_list_uri=dataset_list_uri,
        max_files=max_files,
        compression_filter=compression_filter,
        tile_size=tile_size,
        pixels_per_fragment=PIXELS_PER_FRAGMENT,
        chunk_size=chunk_size,
        nodata=nodata,
        resampling=resampling,
        res=res,
        verbose=verbose,
        trace=trace,
        log_uri=log_uri,
        image_name=DEFAULT_IMG_NAME,
        name=f"{dag_name} input collector",
    )

    # schema creation node, returns a sequence of work items
    ingest_node = graph.submit(
        fn,
        args=input_list_node,
        dataset_uri=dataset_uri,
        config=config,
        append=False,
        batch_size=batch_size,
        stats=stats,
        verbose=verbose,
        trace=trace,
        log_uri=log_uri,
        name=f"{task_prefix} - schema creation",
        mode=tiledb.cloud.dag.Mode.BATCH,
        resources=DEFAULT_RESOURCES,
        image_name=DEFAULT_IMG_NAME,
        access_credentials_name=acn,
    )
    ingest_node.depends_on(input_list_node)

    process_node = graph.submit(
        fn,
        sources=ingest_node,
        dataset_uri=dataset_uri,
        config=config,
        name=task_prefix,
        expand_node_output=ingest_node,
        mode=tiledb.cloud.dag.Mode.BATCH,
        append=True,
        stats=stats,
        verbose=verbose,
        trace=trace,
        log_uri=log_uri,
        resources=DEFAULT_RESOURCES,
        image_name=DEFAULT_IMG_NAME,
        access_credentials_name=acn,
    )

    graph.submit(
        consolidate_meta,
        dataset_uri,
        config=config,
        resources=DEFAULT_RESOURCES,
        verbose=verbose,
        trace=trace,
        log_uri=log_uri,
        access_credentials_name=acn,
    ).depends_on(process_node)

    # Register the dataset on TileDB Cloud
    if register_name:
        graph.submit(
            register_dataset_udf,
            dataset_uri,
            namespace=namespace,
            register_name=register_name,
            config=config,
            verbose=verbose,
            access_credentials_name=acn,
        ).depends_on(process_node)

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
    config: Optional[Mapping[str, object]] = None,
    id: str = "consolidate",
    verbose: bool = False,
    trace: bool = False,
    log_uri: Optional[str] = None,
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
        with Profiler(array_uri=log_uri, id=id, trace=trace):
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
    pixels_per_fragment=PIXELS_PER_FRAGMENT,
    chunk_size: int = POINT_CLOUD_CHUNK_SIZE,
    nodata: Optional[float] = None,
    res: Tuple[float, float] = None,
    stats: bool = False,
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
    :param compression_filter: serialized tiledb filter,
        defaults to None
    :param workers: number of workers for dataset ingestion, defaults to MAX_WORKERS
    :param batch_size: batch size for dataset ingestion, defaults to BATCH_SIZE
    :param tile_size: for rasters this is the tile (block) size
        for the merged destination array defaults to 1024
    :param pixels_per_fragment: for rasters this this the number of tiles
        that will be processed together per fragment. Ideally aim to align
        as a factor of tile_size
    :param chunk_size: for point cloud this is the PDAL chunk size, defaults to 1000000
    :param nodata: NODATA value for rasters
    :param res: Tuple[float, float], output resolution in x/y
    :param stats: bool, print TileDB stats to stdout
    :param verbose: verbose logging, defaults to False
    :param trace: bool, enable trace for logging, defaults to False
    :param log_uri: log array URI
    """

    # Validate user input
    if search_uri and dataset_list_uri:
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
        pixels_per_fragment=pixels_per_fragment,
        chunk_size=chunk_size,
        nodata=nodata,
        res=res,
        stats=stats,
        verbose=verbose,
        trace=trace,
        log_uri=log_uri,
    )


# Wrapper function for batch dataset ingestion
ingest = as_batch(ingest_datasets)

if __name__ == "__main__":
    # date_mark = datetime.now().strftime('%Y%m%d-%H%M%S')
    date_mark = "1"
    ingest_datasets(
        dataset_uri=f"s3://tiledb-norman/deleteme/lidar/ma/2024-03-05/test-{date_mark}",
        dataset_type=DatasetType.POINTCLOUD,
        acn="norman-cloud-sandbox-role",
        namespace="norman",
        register_name="test_lidar_ma",
        search_uri="s3://tiledb-norman/deleteme/files/geospatial/lidar/MA_CentralEastern_2021_B21/",
        stats=False,
        verbose=True,
        trace=True,
        pattern="*.laz",
    )

# if __name__ == "__main__":
#     from tiledb.cloud.utilities import serialize_filter

#     # date_mark = datetime.now().strftime('%Y%m%d-%H%M%S')
#     date_mark = "1"

#     tile_size = 1024
#     pixels_per_fragment = 1024 * 10  # 10 tiles per fragment
#     zstd_filter = tiledb.ZstdFilter(level=7)

#     ingest_datasets(
#         dataset_uri=f"s3://tiledb-norman/deleteme/raster/sentinel-s2-l2a/2024-03-08/test-{date_mark}",
#         dataset_type=DatasetType.RASTER,
#         batch_size=1,
#         tile_size=tile_size,
#         pixels_per_fragment=pixels_per_fragment,
#         nodata=0,
#         compression_filter=serialize_filter(zstd_filter),
#         acn="norman-cloud-sandbox-role",
#         namespace="norman",
#         register_name="test_sentinel_2",
#         search_uri="s3://tiledb-norman/deleteme/files/geospatial/raster/sentinel-s2-l2a-cogs/",
#         stats=False,
#         verbose=True,
#         trace=True,
#         pattern="*.tif",
#     )
