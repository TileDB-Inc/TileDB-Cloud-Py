import math
import os
from dataclasses import dataclass
from typing import Any, Iterator, Mapping, Optional, Sequence, Tuple, Union

import pdal
import rasterio
import shapely
from rtree import index

import tiledb


class RasterIngestionWarning(UserWarning):
    pass

@dataclass
class GeoExtents:
    minx: float
    miny: float
    maxx: float
    maxy: float
    minz: Optional[float] = None
    maxz : Optional[float] = None
    
    @property
    def bounds(self):
        if self.minz:
            return (self.minx, self.miny, self.minz,
                    self.maxx, self.maxy, self.maxz)
        else:
            return (self.minx, self.miny, self.maxx, self.maxy)

@dataclass
class GeoMetadata:
    path: os.PathLike
    extents: GeoExtents
    projection: str
    block_shapes: (1024, 1024)

    def __eq__(self, other):
        if not isinstance(other, GeoMetadata):
            return NotImplemented
        return self.path == other.path

def get_metadata(
    source: Sequence[os.PathLike], config: Mapping[str, Any] = None, **kwargs
) -> Tuple[Union[Tuple[GeoMetadata, ...], Tuple[Tuple[GeoMetadata], ...]], GeoExtents, Tuple[float, float]]:
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

    def group_by_raster_block(meta: Sequence[GeoMetadata]) -> Tuple[tuple[tuple[(int, int), (int, int)], tuple[str, ...]], ...]:
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

        dst_transform = rasterio.transform.from_bounds(*full_extents.bounds, width, height)
        dst_window = rasterio.windows.Window(0, 0, width, height)

        results = []
        for i in range(num_blocks_x):
            for j in range(num_blocks_y):
                # calculate window in local pixel co-ordinates and clamp to destination dimensions
                win = rasterio.windows.Window(i*dst_tile_size, j*dst_tile_size, dst_tile_size, dst_tile_size).intersection(dst_window)
                region_bounds = rasterio.windows.bounds(win, dst_transform)
                # find intersection
                intersects = tuple(idx.intersection(region_bounds))
                if len(intersects) > 0:
                    # append the result in pixel coords
                    results.append((win.toranges(), tuple([meta[s].path for s in intersects])))

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
                # projection information is not always easily available but we will get the extents
                pipeline = pdal.Reader.las(filename=pth).pipeline()
                info = pipeline.quickinfo()
                extents = GeoExtents(**info["stats"]["bbox"]["native"]["bbox"])
            elif pth.suffix[1:] in raster_exts:
                with rasterio.open(pth) as src:
                    extents = GeoExtents(
                        minx=src.bounds[0],
                        miny=src.bounds[1],
                        maxx=src.bounds[2],
                        maxy=src.bounds[3]
                    )

                    # initialization of variables
                    if proj is None:
                        proj = src.crs
                    else:
                        if proj != src.crs:
                            raise ValueError("All datasets need to be in the same projection")
                    
                    if num_channels is None:
                        num_channels = src.count
                    else:
                        if num_channels != src.count:
                            raise ValueError("All datasets need to have the same number of bands")

                    if xres is None:
                        xres, yres = src.res

            if not extents:
                continue

            if full_extents:
                full_extents = GeoExtents(*shapely.unary_union([shapely.box(*full_extents.bounds), shapely.box(*extents.bounds)]).bounds)
            else:
                full_extents = extents
 
            yield GeoMetadata(path=pth, extents=extents, projection=proj, block_shapes=(dst_tile_size, dst_tile_size))

    if len(source) == 1 and vfs.is_dir(source[0]):
        with tiledb.scope_ctx(ctx_or_config=config):
            # Folder like input
            contents = vfs.ls(source[0])
            if len(contents) != 0:
                return group_by_raster_block(tuple(iter_paths(contents))), full_extents, (xres, yres) 
            else: 
                raise ValueError("Input bucket should contain geospatial datasets for ingestion")
    elif isinstance(source, Sequence):
        if len(source) > 0:
            # List of input uris - single file is one element list
            return group_by_raster_block(tuple(iter_paths(source))), full_extents, (xres, yres)
        else:
            raise ValueError("Input sequence should contain geospatial datasets for ingestion")

def serialize_filter(filter):
    if isinstance(filter, tiledb.Filter):
        filter_dict = filter._attrs_()
        filter_dict["_name"] = type(filter).__name__
        return filter_dict
    else:
        raise TypeError


def batch(iterable, chunks):
    # Iterator for providing batches of chunks
    length = len(iterable)
    for ndx in range(0, length, chunks):
        yield iterable[ndx : min(ndx + chunks, length)]


def scale_calc(samples, num_batches):
    """Calculate scaling settings for batch_size and max_workers

    :param source: The source iterable containing files to be ingested/exported
    :param num_batches: The number of batches given by the API
    :return: Tuple batch_size, max_workers
    """
    # If num_batches is default create number of images nodes
    # constraint node max_workers to 20 fully heuristic
    batch_size = 1 if num_batches is None else math.ceil(len(samples) / num_batches)
    max_workers = 20 if num_batches is None else None
    return batch_size, max_workers
