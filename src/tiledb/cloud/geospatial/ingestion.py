import math
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Mapping, Optional, Sequence, Tuple, Union

import fiona
import pdal
import rasterio
import shapely
from rtree import index

import tiledb
from tiledb.cloud import batch
from tiledb.cloud import scale_calc
from tiledb.cloud import serialize_filter
from tiledb.cloud._common.utils import logger

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-geo"
DEFAULT_DAG_NAME = "geo-ingestion"

# fiona.drvsupport.supported_drivers["TileDB"] = "rw"
# fiona.vfs.SCHEMES["tiledb"] = "tiledb"


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
class GeoMetadata:
    path: os.PathLike
    extents: BoundingBox
    crs: str
    block_shapes: (1024, 1024)

    def __eq__(self, other):
        if not isinstance(other, GeoMetadata):
            return NotImplemented
        return self.path == other.path


def get_metadata(
    source: Sequence[os.PathLike], config: Mapping[str, Any] = None, **kwargs
) -> Tuple[
    Union[Tuple[GeoMetadata, ...], Tuple[Tuple[GeoMetadata], ...]],
    BoundingBox,
    Tuple[float, float],
]:
    """Return geospatial metadata for a sequence of input data files

    :param source: A sequence of paths or path to input
    :param config: dict configuration to pass on tiledb.VFS
    """
    vfs = tiledb.VFS(config=config)
    raster_exts = list(rasterio.drivers.raster_driver_extensions().keys())
    pc_exts = [".las", ".laz"]
    full_extents = None
    proj = None
    num_channels = None
    xres = None
    yres = None
    dst_tile_size = kwargs.get("tile_size", 1024)

    def group_by_raster_block(
        meta: Sequence[GeoMetadata],
    ) -> Tuple[tuple[tuple[(int, int), (int, int)], tuple[str, ...]], ...]:
        # fast load of geometries in to a r-tree
        def load_geoms(meta):
            for i, im in enumerate(meta):
                yield (i, im.extents.bounds, None)

        idx = index.Index(load_geoms(meta))
        bounds = tuple(idx.bounds)
        if bounds != full_extents.bounds:
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
                        (win.toranges(), tuple([meta[s].path for s in intersects]))
                    )

        return tuple(results)

    def iter_paths(sequence: Sequence[os.PathLike]) -> Iterator[Tuple]:
        nonlocal full_extents
        nonlocal xres
        nonlocal yres
        nonlocal proj
        nonlocal num_channels

        for pth in sequence:
            extents = None
            if pth.suffix in pc_exts:
                # crs information is not always easily available
                # however we will get the extents
                pipeline = pdal.Reader.las(filename=pth).pipeline()
                info = pipeline.quickinfo()
                extents = BoundingBox(**info["stats"]["bbox"]["native"]["bbox"])
            elif pth.suffix[1:] in raster_exts:
                with rasterio.open(pth) as src:
                    extents = BoundingBox(
                        minx=src.bounds[0],
                        miny=src.bounds[1],
                        maxx=src.bounds[2],
                        maxy=src.bounds[3],
                    )

                    # initialization of variables
                    if proj is None:
                        proj = src.crs
                    else:
                        if proj != src.crs:
                            raise ValueError(
                                "All datasets need to be in the same projection"
                            )

                    if num_channels is None:
                        num_channels = src.count
                    else:
                        if num_channels != src.count:
                            raise ValueError(
                                "All datasets need to have the same number of bands"
                            )

                    if xres is None:
                        xres, yres = src.res

            if not extents:
                continue

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

            yield GeoMetadata(
                path=pth,
                extents=extents,
                crs=proj,
                block_shapes=(dst_tile_size, dst_tile_size),
            )

    if len(source) == 1 and vfs.is_dir(source[0]):
        with tiledb.scope_ctx(ctx_or_config=config):
            # Folder like input
            contents = vfs.ls(source[0])
            if len(contents) != 0:
                return (
                    group_by_raster_block(tuple(iter_paths(contents))),
                    full_extents,
                    (xres, yres),
                )
            else:
                raise ValueError(
                    "Input bucket should contain geospatial datasets for ingestion"
                )
    elif isinstance(source, Sequence):
        if len(source) > 0:
            # List of input uris - single file is one element list
            return (
                group_by_raster_block(tuple(iter_paths(source))),
                full_extents,
                (xres, yres),
            )
        else:
            raise ValueError(
                "Input sequence should contain geospatial datasets for ingestion"
            )


def ingest(
    source: Union[Sequence[str], str],
    output: str,
    config: Mapping[str, Any],
    *args: Any,
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    threads: Optional[int] = 8,
    resources: Optional[Mapping[str, Any]] = None,
    compute: bool = True,
    namespace: Optional[str] = None,
    **kwargs,
) -> Optional[tiledb.cloud.dag.DAG]:
    """The function ingests geospatial point clouds and images into TileDB arrays

    :param source: uri / iterable of uris of input files
    :param output: output TileDB array name
    :param config: dict configuration to pass on tiledb.VFS
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn.
        Performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 8
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"},
        defaults to None
    :param compute: When True the DAG returned will be computed inside the function
    otherwise DAG will only be returned.
    :param namespace: The namespace where the DAG will run
    """

    # flag to test inner functions locally
    unit_testing = kwargs.get("unit_testing", False)

    def consolidate_fragment_meta(output, config):
        """
        Consolidate fragment metadata for point clouds.

        :param output: output TileDB array
        :param config: Mapping[str, Any],
        """
        conf = tiledb.Config(params=config)
        conf["sm.consolidation.mode"] = "fragment_meta"
        ctx = tiledb.Ctx(config)
        tiledb.consolidate(output, ctx=ctx)

    def ingest_geometry_udf(
        input: Sequence[str],
        output: str,
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
        input: Sequence[str],
        output: str,
        *args: Any,
        **kwargs,
    ):
        """Internal udf that ingests server side batch of point cloud files
        into tiledb arrays using PDAL API. Compression uses the default profile
        build in to PDAL.

        :param input: laz/las input file names
        :param output: output TileDB array name
        """

        import pdal

        append = kwargs.get("append", False)

        if not append:
            extents = kwargs.pop("extents", None)
            if extents:
                pipeline = pdal.Writer.tiledb(
                    array_name=output,
                    x_domain_st=extents[0],
                    y_domain_st=extents[1],
                    z_domain_st=extents[2],
                    x_domain_ed=extents[3],
                    y_domain_ed=extents[4],
                    z_domain_ed=extents[5],
                    **kwargs,
                )
            else:
                raise ValueError("Unknown extents for ingestion")
        else:
            for i in input:
                pipeline |= pdal.Reader.las(filename=i)
                pipeline |= pdal.Writer.tiledb(array_name=output, **kwargs)

        pipeline.execute()

    def ingest_raster_udf(
        inputs: Tuple[tuple[(int, int), (int, int)], tuple[str, ...]],
        output: str,
        *args: Any,
        **kwargs,
    ):
        """Internal udf that ingests server side batch of raster files
        into tiledb arrays using Rasterio API

        :param io_uris: raster input file names
        :param output: output TileDB array name
        """

        import rasterio
        import rasterio.merge

        append = kwargs.get("append", False)

        if not append:
            from rasterio.transform import from_origin

            from tiledb import filter

            compressor = kwargs.get("compressor", None)
            extents = kwargs.pop("extents", None)
            tile_size = kwargs.get("tile_size", 1024)
            res = kwargs.pop("res", None)

            if compressor and extents and res:
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

                # create empty array,
                # inputs is a single reference file when creating the array
                with rasterio.open(inputs) as src:
                    dst_profile = src.profile.copy()
                    dst_profile.update(
                        {
                            "driver": "TileDB",
                            "transform": from_origin(extents.minx, extents.maxy, *res),
                            "width": math.floor((extents.maxx - extents.minx) / res[0]),
                            "height": math.floor(
                                (extents.maxy - extents.miny) / res[1]
                            ),
                            "blockysize": tile_size,
                            "blockxsize": tile_size,
                        }
                    )
                    with rasterio.open(
                        output,
                        "w",
                        COMPRESSION=compressor_name[
                            :-6
                        ].upper(),  # remove trailing `Filter`
                        COMPRESSION_LEVEL=compression_level,
                        **dst_profile,
                    ):
                        pass
        else:
            # srcs and dst have same number of bands
            resampling = rasterio.enums.Resampling[
                kwargs.pop("resampling", "bilinear").lower()
            ]
            with rasterio.open(output, mode="r+") as dst:
                for blk, srcs in inputs:
                    input_datasets = []
                    try:
                        input_datasets.extend([rasterio.open(s) for s in srcs])
                        row_off = blk[0][0]
                        col_off = blk[1][0]
                        dst_window = rasterio.windows.Window(
                            col_off,
                            row_off,
                            blk[1][1] - col_off,
                            blk[0][1] - row_off,
                        )
                        dst_bounds = rasterio.windows.bounds(dst_window, dst.transform)

                        for b in range(dst.count):
                            if len(srcs) == 1:
                                with rasterio.vrt.WarpedVRT(
                                    input_datasets[0],
                                    crs=dst.crs,
                                    transform=dst.transform,
                                    resampling=resampling,
                                    width=dst.width,
                                    height=dst.height,
                                    masked=True,
                                ) as vrt:
                                    # TODO fix this duplication of requests
                                    # over multiple bands with a single call to merge
                                    data = vrt.read(window=dst_window)
                                    dst.write(data[b], window=dst_window, indexes=b + 1)
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

    if isinstance(source, str):
        # Handle only lists
        source = [source]

    fn = None

    # enable ingestion of las or laz LiDAR point clouds
    ext = os.path.splitext(source[0])[1][1:].lower()
    if ext == "las" or ext == "laz":
        fn = ingest_point_cloud_udf

    try:
        if not fn:
            rasterio.driver_from_extension(source[0])
            fn = ingest_raster_udf
    except ValueError:
        pass

    try:
        if not fn:
            fiona.drvsupport.driver_from_extension(source[0])
            fn = ingest_geometry_udf
    except ValueError:
        pass

    if not fn:
        raise ValueError(f"{source[0]} is not supported for ingestion.")

    # Get the list of all geospatial input/out
    samples, full_extents, res = get_metadata(source, config=config, **kwargs)
    batch_size, max_workers = scale_calc(samples, num_batches)

    if len(samples) == 0:
        raise ValueError("No recognized datasets for ingestion")

    # take a sample so that the tildb schema can be quickly created
    init_path = samples[0][1][0]

    # serialize compressor udf arguments for raster and geometry
    compressor = kwargs.pop("compressor", None)
    compressor_serial = serialize_filter(compressor) if compressor else None

    if not unit_testing:
        # Build the task graph
        dag_name = taskgraph_name or DEFAULT_DAG_NAME
        task_prefix = f"{dag_name} - Task"

        logger.info("Building graph")
        graph = tiledb.cloud.dag.DAG(
            name=dag_name,
            mode=tiledb.cloud.dag.Mode.BATCH,
            max_workers=max_workers,
            namespace=namespace,
        )

        nodes = []

        # create first node
        ingest_node = graph.submit(
            fn,
            init_path,  # used to copy the raster profile
            output,
            config,
            threads,
            *args,
            name=f"{task_prefix} - {0}/{num_batches}",
            mode=tiledb.cloud.dag.Mode.BATCH,
            resources=DEFAULT_RESOURCES if resources is None else resources,
            image_name=DEFAULT_IMG_NAME,
            compressor=compressor_serial,
            extents=full_extents,
            res=res,
            append=False**kwargs,
        )

        for i, work in enumerate(batch(samples, batch_size)):
            logger.info(f"Adding batch {i + 1}")
            n = graph.submit(
                fn,
                work,
                output,
                config,
                threads,
                *args,
                name=f"{task_prefix} - {i + 1}/{num_batches}",
                mode=tiledb.cloud.dag.Mode.BATCH,
                resources=DEFAULT_RESOURCES if resources is None else resources,
                image_name=DEFAULT_IMG_NAME,
                append=True**kwargs,
            )

            n.depends_on(ingest_node)
            nodes.append(n)

        graph.submit(
            consolidate_fragment_meta,
            output,
            config,
            threads,
            *args,
            name=f"{task_prefix} - metadata consolidation",
            mode=tiledb.cloud.dag.Mode.BATCH,
            resources=DEFAULT_RESOURCES if resources is None else resources,
            image_name=DEFAULT_IMG_NAME,
            **kwargs,
        ).depends_on(nodes)

        if compute:
            graph.compute()

        return graph
    else:
        # unit test inner functions
        # set up function
        fn(
            inputs=init_path,  # used to copy the raster profile
            output=output,
            append=False,
            compressor=compressor_serial,
            extents=full_extents,
            res=res,
            *args,
            **kwargs,
        )
        # work functions
        for i, work in enumerate(batch(samples, batch_size)):
            fn(inputs=work, output=output, append=True, *args, **kwargs)


def ingest_udf(*args: Any, **kwargs: Any) -> Dict[str, str]:
    """Ingestor wrapper function that can be used as a UDF."""
    grf = ingest(*args, **kwargs)
    return {"status": "started", "graph_id": str(grf.server_graph_uuid)}
