import math
import os
from enum import Enum
from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

import attrs

import tiledb
from tiledb.cloud.files import utils as file_utils
from tiledb.cloud.utilities import Profiler
from tiledb.cloud.utilities import as_batch
from tiledb.cloud.utilities import chunk
from tiledb.cloud.utilities import create_log_array
from tiledb.cloud.utilities import find
from tiledb.cloud.utilities import get_logger_wrapper
from tiledb.cloud.utilities import max_memory_usage
from tiledb.cloud.utilities import run_dag

DEFAULT_RESOURCES = {"cpu": "2", "memory": "2Gi"}
DEFAULT_IMG_NAME = "3.9-geo"
DEFAULT_DAG_NAME = "geo-ingestion"

# Default values for ingestion parameters
RASTER_TILE_SIZE = 1024
PIXELS_PER_FRAGMENT = (RASTER_TILE_SIZE**2) * 10
DEFAULT_RASTER_SAMPLING = "bilinear"
POINT_CLOUD_CHUNK_SIZE = 1_000_000
GEOMETRY_CHUNK_SIZE = 100_000
MAX_WORKERS = 40
BATCH_SIZE = 10

XYZBoundsTuple = Tuple[float, float, float, float, float, float]
XYBoundsTuple = Tuple[float, float, float, float]
XYZTuple = Tuple[float, float, float]
XYTuple = Tuple[float, float]


class DatasetType(Enum):
    POINTCLOUD = "POINTCLOUD"
    RASTER = "RASTER"
    GEOMETRY = "GEOMETRY"


def _sanitize_dataset_type(value: Any) -> DatasetType:
    try:
        return DatasetType(value)
    except ValueError:
        raise ValueError(f"{value} is nto a valid Dataset Type")


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

    @property
    def mins(self) -> Union[XYTuple, XYZTuple]:
        if self.minz:
            return (self.minx, self.miny, self.minz)
        else:
            return (self.minx, self.miny)

    @property
    def maxs(self) -> Union[XYTuple, XYZTuple]:
        if self.maxz:
            return (self.maxx, self.maxy, self.maxz)
        else:
            return (self.maxx, self.maxy)


@attrs.define
class GeoBlockMetadata:
    ranges: Tuple[Tuple[int, int], Tuple[int, int]]
    files: Tuple[os.PathLike, ...] = attrs.field(converter=tuple)


T = TypeVar("T", int, float)


def _fold_in(oper: Callable, existing: List[T], new: List[T]) -> List[T]:
    if existing is None:
        return new
    return [oper(e) for e in zip(existing, new)]


@attrs.define
class GeoMetadata:
    # common properties
    extents: BoundingBox
    crs: str = None
    path: str = None
    # raster properties
    dtype: Optional[str] = None
    band_count: Optional[int] = None
    res: Optional[Tuple[float, float]] = None
    nodata: Optional[Union[int, float]] = None
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
) -> Sequence[GeoMetadata]:
    """Return geospatial metadata for a sequence of input point cloud data files

    :param sources: iterator, paths or path to process
    :param config: dict, configuration to pass on tiledb.VFS
    :param verbose: bool, enable verbose logging, default is False
    :param trace: bool, enable trace logging, default is False
    :param log_uri: Optional[str] = None,
    :Return: list[GeoMetadata], a list of populated GeoMetadata objects
    """
    import laspy

    if not sources:
        raise ValueError("Input point cloud datasets required")

    with tiledb.scope_ctx(config):
        vfs = tiledb.VFS()
        logger = get_logger_wrapper(verbose)
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            meta = []
            mins = None
            maxs = None

            for f in sources:
                logger.debug("finding metadata for %r", f)
                with vfs.open(f, "rb") as src:
                    # only open header
                    las = laspy.open(src)
                    hdr = las.header
                    mins = _fold_in(min, mins, hdr.mins)
                    maxs = _fold_in(max, maxs, hdr.maxs)
                    meta.append(
                        GeoMetadata(
                            path=f,
                            extents=BoundingBox(
                                minx=hdr.mins[0],
                                miny=hdr.mins[1],
                                minz=hdr.mins[2],
                                maxx=hdr.maxs[0],
                                maxy=hdr.maxs[1],
                                maxz=hdr.maxs[2],
                            ),
                            scales=tuple(hdr.scales),
                            offsets=tuple(hdr.offsets),
                        )
                    )

            return meta


def load_geometry_metadata(
    sources: Iterable[os.PathLike],
    *,
    config: Optional[Mapping[str, object]] = None,
    verbose: bool = False,
    id: str = "pointcloud_metadata",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> Sequence[GeoMetadata]:
    """Return geospatial metadata for a sequence of input geometry data files

    :param sources: A sequence of paths or path to input
    :param config: dict configuration to pass on tiledb.VFS
    :param verbose: bool, enable verbose logging, default is False
    :param trace: bool, enable trace logging, default is False
    :param log_uri: Optional[str] = None,
    :Return: list[GeoMetadata], a list of populated GeoMetadata objects
    """
    # note this will be refactored to use /vsipyopener in fiona
    import fiona

    fiona.drvsupport.supported_drivers["TileDB"] = "arw"
    fiona.vfs.SCHEMES["tiledb"] = "tiledb"

    if not sources:
        raise ValueError("Input point cloud datasets required")

    with tiledb.scope_ctx(config):
        vfs = tiledb.VFS()
        logger = get_logger_wrapper(verbose)
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            # for geometries we need the maximum extents
            # and to check geometry types / crs are the same
            meta = []
            for pth in sources:
                logger.debug("finding metadata for %r", pth)
                with fiona.open(pth, opener=vfs.open) as src:
                    # 2.5 is supported internally but not needed for ingest
                    extents = BoundingBox(
                        minx=src.bounds[0],
                        miny=src.bounds[1],
                        maxx=src.bounds[2],
                        maxy=src.bounds[3],
                    )
                    meta.append(
                        GeoMetadata(
                            extents=extents,
                            crs=src.crs,
                            path=pth,
                            geometry_schema=src.schema,
                        )
                    )

            return meta


def load_raster_metadata(
    sources: Iterable[os.PathLike],
    *,
    config: Optional[Mapping[str, object]] = None,
    verbose: bool = False,
    id: str = "raster_metadata",
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> Sequence[GeoMetadata]:
    """Return geospatial metadata for a sequence of input raster data files

    :param sources: iterator, paths or path to process
    :param config: dict, configuration to pass on tiledb.VFS
    :param verbose: bool, enable verbose logging, default is False
    :param trace: bool, enable trace logging, default is False
    :param id: str, ID for logging
    :param log_uri: Optional[str] = None,
    :Return: list[GeoMetadata]: list of populated GeoMetadata objects
    """
    import rasterio

    if not sources:
        raise ValueError("Input raster datasets required")

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            meta = []
            vfs = tiledb.VFS(config=config)

            for pth in sources:
                logger.debug("Including %r", pth)
                with rasterio.open(pth, opener=vfs.open) as src:
                    extents = BoundingBox(
                        minx=src.bounds[0],
                        miny=src.bounds[1],
                        maxx=src.bounds[2],
                        maxy=src.bounds[3],
                    )

                    logger.debug("Extents for %r %r", pth, extents)
                    m = GeoMetadata(
                        extents=extents,
                        crs=src.crs,
                        path=pth,
                        dtype=src.profile["dtype"],
                        res=src.res,
                        band_count=src.count,
                        nodata=src.nodata,
                    )
                    meta.append(m)

            if not meta:
                raise ValueError("Raster datasets not found")

            return meta


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
    :param id: str, ID for logging
    :param trace, bool, enable trace logging
    :param log_uri: log array URI
    :return: if not appending then the function returns a tuple of file paths
    """
    import fiona
    import shapely

    from tiledb import filter

    if not append and args:
        # first map the args from the previous stage
        sources = []
        arg = args[0]
        schema = arg["schema"]
        crs = arg["crs"]
        if compressor in arg:
            compressor = arg["compressor"]
        if chunk_size in arg:
            chunk_size = arg["chunk_size"]
        extents = None
        for d in args:
            for s in d["sources"]:
                m: GeoMetadata = s
                sources.append(m.path)
                if not extents:
                    extents = m.extents
                else:
                    exts = m.extents
                    extents = BoundingBox(
                        *shapely.unary_union(
                            [
                                shapely.box(*extents.bounds),
                                shapely.box(*exts.bounds),
                            ]
                        ).bounds
                    )

    if append and args:
        sources = args["sources"]

    with tiledb.scope_ctx(config):
        with Profiler(array_uri=log_uri, id=id, trace=trace):
            vfs = tiledb.VFS()
            logger = get_logger_wrapper(verbose)
            try:
                if append:
                    for f in sources:
                        logger.debug("ingesting geometry dataset %r", f)
                        with fiona.open(f, opener=vfs.open) as colxn:
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
                            BOUNDS=",".join(str(v) for v in extents.bounds),
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
                            BOUNDS=",".join(str(v) for v in extents.bounds),
                        ) as dst:
                            pass

                    return [{"sources": s} for s in chunk(sources, batch_size)]
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
    sources: Sequence[GeoMetadata] = None,
    append: bool = False,
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

    :param args: dict or list, input key value arguments as a dictionary
    :param dataset_uri: str, output TileDB array name
    :param sources: Sequence of GeoMetadata objects
    :param append: bool, whether to append to the array
    :param chunk_size: PDAL configuration for chunking fragments
    :param batch_size: batch size for dataset ingestion, defaults to BATCH_SIZE
    :param verbose: verbose logging, defaults to False
    :param stats: bool, print TileDB stats to stdout
    :param config: dict, configuration to pass on tiledb.VFS
    :param id: str, ID for logging
    :param trace, bool, enable trace logging
    :param log_uri: log array URI
    :return: if not appending then a sequence of file paths
    """
    import laspy
    import numpy as np
    import pdal

    if not append and args:
        # first map the args from the previous stage
        sources = []
        arg = args[0]
        if chunk_size in arg:
            chunk_size = arg["chunk_size"]
        if batch_size in arg:
            batch_size = arg["batch_size"]

        mins = None
        maxs = None
        offsets = None
        scales = None

        for d in args:
            for s in d["sources"]:
                m: GeoMetadata = s
                sources.append(m.path)

                mins = _fold_in(min, mins, m.extents.mins)
                maxs = _fold_in(max, maxs, m.extents.maxs)

                if m.offsets:
                    offsets = _fold_in(min, offsets, m.offsets)

                if m.scales:
                    scales = _fold_in(max, scales, m.scales)

        extents = BoundingBox(
            minx=mins[0],
            miny=mins[1],
            minz=mins[2],
            maxx=maxs[0],
            maxy=maxs[1],
            maxz=maxs[2],
        )

    if append and args:
        sources = args["sources"]

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

                if extents:
                    template_sample = sources[0]
                    logger.debug("creating point cloud schema from %r", template_sample)
                    with vfs.open(template_sample, "rb") as src:
                        las = laspy.open(src)
                        chunk_itr = las.chunk_iterator(chunk_size)
                        first_chunk = next(chunk_itr)
                        arr = get_pc_array(first_chunk)
                        if offsets and scales:
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
                        else:
                            pipeline = pdal.Writer.tiledb(
                                array_name=dataset_uri,
                                x_domain_st=extents.minx - 1,
                                y_domain_st=extents.miny - 1,
                                z_domain_st=extents.minz - 1,
                                x_domain_end=extents.maxx + 1,
                                y_domain_end=extents.maxy + 1,
                                z_domain_end=extents.maxz + 1,
                                chunk_size=chunk_size,
                            ).pipeline(arr)

                        pipeline.execute()

                        for c in chunk_itr:
                            arr = get_pc_array(c)
                            pipeline = pdal.Writer.tiledb(
                                array_name=dataset_uri, stats=stats, append=True
                            ).pipeline(arr)
                            pipeline.execute()

                    return [{"sources": s} for s in chunk(sources[1:], batch_size)]
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
    nodata: Optional[float] = None,
    pixels_per_fragment: int = PIXELS_PER_FRAGMENT,
    tile_size: int = RASTER_TILE_SIZE,
    resampling: str = DEFAULT_RASTER_SAMPLING,
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
    :param nodata: float, NODATA value for destination raster
    :param tile_size: for rasters this is the tile (block) size
        for the merged destination array, defaults to 1024
    :param pixels_per_fragment: This is the number of pixels that will be
        written per fragment. Ideally aim to align as a factor of tile_size
    :param resampling: string, resampling method,
        one of None, bilinear, cubic, nearest and average
    :param append: bool, whether to append to the array
    :param batch_size: batch size for dataset ingestion, defaults to BATCH_SIZE
    :param stats: bool, print TileDB stats to stdout
    :param verbose: verbose logging, defaults to False
    :param config: dict, configuration to pass on tiledb.VFS
    :param compressor: dict, serialized compression filter
    :param id: str, ID for logging
    :param trace, bool, enable trace logging
    :param log_uri: log array URI
    :return: if not appending then a sequence of populated GeoBlockMetadata objects
    """

    import rasterio
    import rasterio.merge
    import shapely
    from rtree import index

    logger = get_logger_wrapper(verbose)
    if not append and args:
        # first map the args from the previous stage
        arg = args[0]
        meta: GeoMetadata = args[0]["sources"][0]
        band_count = meta.band_count
        crs = meta.crs
        dtype = meta.dtype
        nodata = arg["nodata"] if "nodata" in arg else nodata
        res = arg["res"] if "res" in arg else meta.res
        resampling = (
            arg["resampling"] if "resampling" in arg else DEFAULT_RASTER_SAMPLING
        )
        tile_size = arg["tile_size"]
        batch_size = arg["batch_size"] if "batch_size" in arg else batch_size
        compressor = arg["compressor"] if "compressor" in arg else None
        pixels_per_fragment = (
            arg["pixels_per_fragment"]
            if "pixels_per_fragment" in arg
            else pixels_per_fragment
        )

        extents = None

        idx = index.Index()
        id = 0
        blocks = []

        for d in args:
            for m in d["sources"]:
                if m.crs != crs:
                    raise ValueError("All datasets need to be in the same CRS")

                if m.band_count != band_count:
                    raise ValueError(
                        "All datasets need to have the same number of bands"
                    )

                if not extents:
                    extents = BoundingBox(*m.extents.bounds)
                else:
                    exts = m.extents
                    extents = BoundingBox(
                        *shapely.unary_union(
                            [
                                shapely.box(*extents.bounds),
                                shapely.box(*exts.bounds),
                            ]
                        ).bounds
                    )

                # update rtree
                idx.insert(id, m.extents.bounds, obj=m.path)
                id += 1

        width = (extents.bounds[2] - extents.bounds[0]) / res[0]
        height = (extents.bounds[3] - extents.bounds[1]) / res[1]

        dst_windows = rasterio.windows.window_split(height, width, pixels_per_fragment)
        dst_transform = rasterio.transform.from_bounds(*extents.bounds, width, height)

        for _, w in dst_windows:
            region_bounds = rasterio.windows.bounds(w, dst_transform)
            # find intersection
            intersects = tuple(idx.intersection(region_bounds, objects=True))
            if intersects:
                # append the result
                blocks.append(
                    GeoBlockMetadata(
                        ranges=w.toranges(),
                        files=[s.object for s in intersects],
                    )
                )

    if append and args:
        sources = args["sources"]
        resampling = (
            args["resampling"] if resampling in args else DEFAULT_RASTER_SAMPLING
        )
        nodata = args["nodata"] if "nodata" in args else nodata

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
                    return [{"sources": b} for b in chunk(blocks, batch_size)]

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
                                "Written %r coords %r bounds to %r",
                                chunk_window,
                                chunk_bounds,
                                dataset_uri,
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


def build_file_list_udf(
    *,
    dataset_type: DatasetType,
    config: Optional[Mapping[str, object]] = None,
    search_uri: Optional[str] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    dataset_list_uri: Optional[str] = None,
    max_files: Optional[int] = None,
    verbose: bool = False,
    trace: bool = False,
    log_uri: Optional[str] = None,
) -> Sequence[str]:
    """Build a list of sources
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
    :param verbose: verbose logging, defaults to False
    :param trace: bool, enabling log tracing, defaults to False
    :param log_uri: log array URI
    :return: A sequence of source files grouped into batches
    """
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

            dataset_type = _sanitize_dataset_type(dataset_type)
            fns = {
                DatasetType.POINTCLOUD: {
                    "pattern_fn": pointcloud_match,
                },
                DatasetType.RASTER: {
                    "pattern_fn": raster_match,
                },
                DatasetType.GEOMETRY: {
                    "pattern_fn": geometry_match,
                },
            }

            if dataset_list_uri:
                sources = read_uris(
                    dataset_list_uri,
                    dataset_type=dataset_type,
                    log_uri=log_uri,
                    config=config,
                    max_files=max_files,
                )

            if search_uri:
                if pattern:
                    pattern = partial(file_utils.basename_match, pattern=pattern)
                else:
                    pattern = fns[dataset_type]["pattern_fn"]
                if ignore:
                    ignore = partial(file_utils.basename_match, pattern=ignore)

                sources = find(
                    search_uri,
                    config=config,
                    exclude=ignore,
                    include=pattern,
                    max_count=max_files,
                )

            if not sources:
                raise ValueError(f"No {dataset_type.name} datasets found")

            return list(chunk(list(sources), BATCH_SIZE))
        finally:
            logger.info("max memory usage: %.3f GiB", max_memory_usage() / (1 << 30))


def build_inputs_udf(
    *,
    dataset_type: DatasetType,
    sources: Sequence[str],
    config: Optional[Mapping[str, object]] = None,
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
    :param sources: URIs to process
    :param config: config dictionary, defaults to None
    :param compression_filter: serialized tiledb filter,
        defaults to None
    :param tile_size: for rasters this is the tile (block) size
        for the merged destination array, defaults to 1024
    :param pixels_per_fragment: This is the number of pixels that will be
           written per fragment. Ideally aim to align as a factor of tile_size
    :param chunk_size: for point cloud this is the PDAL chunk size, defaults to 1000000
    :param nodata: NODATA value for raster merging
    :param resampling: string, resampling method,
        one of None, bilinear, cubic, nearest and average
    :param res: Tuple[float, float], output resolution in x/y
    :param verbose: verbose logging, defaults to False
    :param trace: bool, enabling log tracing,    to False
    :param log_uri: log array URI
    :return: A dict containing the kwargs needed for the next function call
    """
    logger = get_logger_wrapper(verbose)
    with Profiler(array_uri=log_uri, id=id, trace=trace):
        try:
            dataset_type = _sanitize_dataset_type(dataset_type)
            fns = {
                DatasetType.POINTCLOUD: {
                    "meta_fn": load_pointcloud_metadata,
                },
                DatasetType.RASTER: {
                    "meta_fn": load_raster_metadata,
                },
                DatasetType.GEOMETRY: {
                    "meta_fn": load_geometry_metadata,
                },
            }

            kwargs = {}

            meta = fns[dataset_type]["meta_fn"](sources, config=config)

            if dataset_type == DatasetType.POINTCLOUD:
                kwargs.update(
                    chunk_size=chunk_size,
                    sources=meta,
                )
            elif dataset_type == DatasetType.RASTER:
                if res is None:
                    res = meta[0].res
                kwargs.update(
                    res=res,
                    pixels_per_fragment=pixels_per_fragment,
                    nodata=nodata,
                    resampling=resampling,
                    tile_size=tile_size,
                    compressor=compression_filter,
                    sources=meta,
                )
            elif dataset_type == DatasetType.GEOMETRY:
                kwargs.update(
                    crs=meta[0].crs,
                    chunk_size=chunk_size,
                    compressor=compression_filter,
                    schema=meta[0].geometry_schema,
                    sources=meta,
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
    pixels_per_fragment: int = PIXELS_PER_FRAGMENT,
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
    :param pixels_per_fragment: This is the number of pixels that will be
           written per fragment. Ideally aim to align as a factor of tile_size
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

    dataset_type = _sanitize_dataset_type(dataset_type)
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

    # first find sources to pass to build_inputs_udf
    file_list_node = graph.submit(
        build_file_list_udf,
        dataset_type=dataset_type,
        access_credentials_name=acn,
        config=config,
        search_uri=search_uri,
        pattern=pattern,
        ignore=ignore,
        dataset_list_uri=dataset_list_uri,
        max_files=max_files,
        image_name=DEFAULT_IMG_NAME,
        name=f"{dag_name} source finder",
    )

    input_list_node = graph.submit(
        build_inputs_udf,
        dataset_type=dataset_type,
        access_credentials_name=acn,
        config=config,
        sources=file_list_node,
        compression_filter=compression_filter,
        tile_size=tile_size,
        pixels_per_fragment=pixels_per_fragment,
        chunk_size=chunk_size,
        nodata=nodata,
        resampling=resampling,
        res=res,
        verbose=verbose,
        trace=trace,
        log_uri=log_uri,
        image_name=DEFAULT_IMG_NAME,
        name=f"{dag_name} input collector",
        expand_node_output=file_list_node,
    )

    input_list_node.depends_on(file_list_node)

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
        args=ingest_node,
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
    process_node.depends_on(ingest_node)

    # FIXME: Temporary fix to remove array dataset_type
    clean_dataset_type = graph.submit(
        remove_dataset_type_from_array_meta,
        dataset_uri,
        verbose=verbose,
        resources=DEFAULT_RESOURCES,
        access_credentials_name=acn,
    )
    clean_dataset_type.depends_on(process_node)

    graph.submit(
        consolidate_meta,
        dataset_uri,
        config=config,
        resources=DEFAULT_RESOURCES,
        verbose=verbose,
        trace=trace,
        log_uri=log_uri,
        access_credentials_name=acn,
    ).depends_on(clean_dataset_type)

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
        ).depends_on(clean_dataset_type)

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


def remove_dataset_type_from_array_meta(
    dataset_uri: str,
    *,
    verbose: bool = False,
):
    """
    Removes `dataset_type` meta if the ingested result is an array.
    FIXME: This exists to fix an internal UI issue until formally fixed.
    FIXME: Related ticket -> sc-48098

    :param dataset_uri: dataset URI
    :param verbose: verbose logging, defaults to False
    """
    logger = get_logger_wrapper(verbose)
    if tiledb.object_type(dataset_uri) == "array":
        logger.info(
            "Removing non-standard dataset_type from ingested array metadata: "
            "dataset_uri=%r",
            dataset_uri,
        )
        with tiledb.open(dataset_uri, mode="w") as array:
            try:
                del array.meta["dataset_type"]
            except KeyError as exc:
                logger.info(
                    f"sc-48098: Failed to remove `dataset_type` key: {str(exc)}"
                )


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
    pixels_per_fragment: int = PIXELS_PER_FRAGMENT,
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
    :param pixels_per_fragment: This is the number of pixels that will be
           written per fragment. Ideally aim to align as a factor of tile_size
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
