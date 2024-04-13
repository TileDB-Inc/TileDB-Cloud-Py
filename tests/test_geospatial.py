import glob
import json
import os
import pathlib
import tempfile
import unittest
import warnings
from enum import Enum
from unittest import mock

import numpy as np
import pytest

import tiledb
import tiledb.cloud.utilities as utils
from tiledb.vfs import VFS

RASTER_NAMES = [
    "test1.tif",
    "test2.tif",
    "test3.tif",
    "test_diff_res.tif",
    "test_diff_crs.tif",
]

PC_NAMES = glob.glob(
    f"{os.path.join(os.path.dirname(__file__), 'data', 'geospatial')}/*.las"
)

GEOM_NAMES = ["test1.geojson", "test2.geojson", "test3.geojson"]


@pytest.mark.geospatial
def run_local(dataset_uri: str, *, dataset_type: Enum, batch_size: int, **kwargs):
    import tiledb.cloud.geospatial as geo

    pixels_per_fragment = None
    nodata = None

    # run the key functions of the DAG locally in sequence
    funcs = {
        geo.DatasetType.POINTCLOUD: {
            "udf_fn": geo.ingest_point_cloud_udf,
        },
        geo.DatasetType.RASTER: {
            "udf_fn": geo.ingest_raster_udf,
        },
        geo.DatasetType.GEOMETRY: {
            "udf_fn": geo.ingest_geometry_udf,
        },
    }

    fn = funcs[dataset_type]["udf_fn"]

    if "pixels_per_fragment" in kwargs:
        pixels_per_fragment = kwargs.pop("pixels_per_fragment")

    if "nodata" in kwargs:
        nodata = kwargs.pop("nodata")

    # unit test inner functions
    sources = geo.build_file_list_udf(
        config=kwargs["config"],
        dataset_type=dataset_type,
        dataset_list_uri=kwargs["dataset_list_uri"],
    )

    kwargs.pop("dataset_list_uri")
    new_kwargs = []

    for s in sources:
        kwargs["sources"] = s
        if pixels_per_fragment:
            kwargs["pixels_per_fragment"] = pixels_per_fragment

        if nodata:
            kwargs["nodata"] = nodata

        new_kwargs.append(
            geo.build_inputs_udf(
                dataset_type=dataset_type,
                **kwargs,
            )
        )

    # schema creation function
    # args will be a list from the result from the metadata returned by build_inputs_udf
    samples = fn(
        dataset_uri=dataset_uri,
        append=False,
        batch_size=batch_size,
        args=new_kwargs,
    )

    # work functions
    for _, work_args in enumerate(samples):
        fn(
            dataset_uri=dataset_uri,
            append=True,
            args=work_args,
        )


@pytest.mark.geospatial
def create_test_geometries(tmp_path: os.PathLike):
    import shapely

    radius = 1.0
    for i in range(1, 4):
        g = shapely.Point(i, i).buffer(radius)
        with open(tmp_path.joinpath(GEOM_NAMES[i - 1]), "w") as dst:
            json.dump(shapely.geometry.mapping(g), dst)


@pytest.mark.geospatial
def create_test_rasters(tmp_path: os.PathLike):
    import affine
    import rasterio

    kwargs = {
        "crs": "EPSG:4326",
        "transform": affine.Affine(0.2, 0, -114, 0, -0.2, 46),
        "count": 1,
        "dtype": rasterio.uint8,
        "driver": "GTiff",
        "width": 10,
        "height": 10,
    }

    # test1 and test2 overlap, test3 is distinct
    # test2 contains nodata which will write over test1
    # we will adjust c and f in the affine transform
    with rasterio.open(tmp_path.joinpath(RASTER_NAMES[0]), "w", **kwargs) as dst:
        data = np.ones((10, 10), dtype=rasterio.uint8)
        dst.write(data, indexes=1)

    kwargs["transform"] = affine.Affine(0.2, 0, -113, 0, -0.2, 45)

    with rasterio.open(tmp_path.joinpath(RASTER_NAMES[1]), "w", **kwargs) as dst:
        data = np.ones((10, 10), dtype=rasterio.uint8) * 2
        data[:5, :5] = 255  # default TileDB nodata
        dst.write(data, indexes=1)

    # distinct from test1 and test2 above
    kwargs["transform"] = affine.Affine(0.2, 0, -100, 0, -0.2, 35)

    with rasterio.open(tmp_path.joinpath(RASTER_NAMES[2]), "w", **kwargs) as dst:
        data = np.ones((10, 10), dtype=rasterio.uint8) * 3
        dst.write(data, indexes=1)

    # write a different resolution
    kwargs["transform"] = affine.Affine(0.3, 0, -100, 0, -0.3, 35)
    with rasterio.open(tmp_path.joinpath(RASTER_NAMES[3]), "w", **kwargs) as dst:
        data = np.ones((10, 10), dtype=rasterio.uint8) * 3
        dst.write(data, indexes=1)

    # write a different crs
    kwargs["crs"] = "EPSG:3857"
    kwargs["transform"] = affine.Affine(0.2, 0, 1000, 0, -0.2, 1000)
    with rasterio.open(tmp_path.joinpath(RASTER_NAMES[4]), "w", **kwargs) as dst:
        data = np.ones((10, 10), dtype=rasterio.uint8) * 4
        dst.write(data, indexes=1)


@pytest.mark.geospatial
class GeospatialTest(unittest.TestCase):
    def setUp(self):
        # Ignore warnings
        warnings.simplefilter("ignore")
        # Create a temporary directory
        self.tempdir_obj = tempfile.TemporaryDirectory()
        self.test_dir = pathlib.Path(self.tempdir_obj.name)

        create_test_rasters(self.test_dir)

        for r in RASTER_NAMES:
            self.assertTrue(os.path.exists(self.test_dir.joinpath(r)))

        create_test_geometries(self.test_dir)
        for g in GEOM_NAMES:
            self.assertTrue(os.path.exists(self.test_dir.joinpath(g)))

        self.out_path = "out"

    def test_raster_load_metadata(self):
        import tiledb.cloud.geospatial as geo

        tile_size = 16
        tile_size**2
        ingest_uri_sample = {
            "test1": [self.test_dir.joinpath(r) for r in RASTER_NAMES[:3]],
            "test2": [],
            "test3": [self.test_dir.joinpath(r) for r in RASTER_NAMES[:4]],
            "test4": [
                self.test_dir.joinpath(RASTER_NAMES[0]),
                self.test_dir.joinpath(RASTER_NAMES[3]),
            ],
        }

        # Rasters
        # Case 1-1 Ingestion
        test_1 = ingest_uri_sample["test1"]
        with mock.patch.object(VFS, "ls", return_value=test_1):
            meta_1 = geo.load_raster_metadata(test_1)
            self.assertEqual(len(meta_1), 3)

            # test the first return value
            self.assertEqual(meta_1[0].path, test_1[0])

        # Case 1-2 Ingestion - Empty input list
        with mock.patch.object(VFS, "ls", return_value=ingest_uri_sample["test2"]):
            # Empty input list raises error
            with self.assertRaises(ValueError):
                geo.load_raster_metadata(ingest_uri_sample["test2"])

    def test_pointcloud_load_metadata(self):
        import tiledb.cloud.geospatial as geo

        with mock.patch.object(VFS, "ls", return_value=PC_NAMES):
            meta_1 = geo.load_pointcloud_metadata(PC_NAMES)
            self.assertEqual(len(meta_1), 11)
            self.assertEqual(meta_1[0].scales, (0.01, 0.01, 0.01))
            self.assertEqual(meta_1[0].offsets, (0.0, 0.0, 0.0))

    def test_geometry_load_metadata(self):
        import fiona

        import tiledb.cloud.geospatial as geo

        geom_names = [self.test_dir.joinpath(g) for g in GEOM_NAMES]
        with mock.patch.object(VFS, "ls", return_value=geom_names):
            meta_1 = geo.load_geometry_metadata(geom_names)
            self.assertEqual(meta_1[0].geometry_schema["geometry"], "Polygon")
            self.assertEqual(meta_1[0].crs, fiona.crs.CRS.from_epsg(4326))

    def test_raster_ingest(self):
        import rasterio

        import tiledb.cloud.geospatial as geo

        tile_size = 16
        pixels_per_fragment = 16**2
        zstd_filter = tiledb.ZstdFilter(level=7)
        test_1 = [self.test_dir.joinpath(r) for r in RASTER_NAMES[:3]]
        with mock.patch.object(VFS, "ls", return_value=test_1):
            expected_extents = geo.BoundingBox(minx=-114, miny=33, maxx=-98, maxy=46)
            output_array = str(self.test_dir.joinpath("raster_output_array"))
            # keep - used to verify output if needed
            # import shutil

            # output_array = "/tmp/output_array"
            # if os.path.exists(output_array):
            #     shutil.rmtree(output_array)

            dataset_list_uri = self.test_dir.joinpath("manifest.txt")
            with open(dataset_list_uri, "w") as f:
                for img in test_1:
                    f.write(f"{img}\n")

            run_local(
                dataset_uri=output_array,
                dataset_type=geo.DatasetType.RASTER,
                config={},
                dataset_list_uri=dataset_list_uri,
                compression_filter=utils.serialize_filter(zstd_filter),
                nodata=255,
                # set batch size to 1 to test overlapping images
                batch_size=1,
                # pick a size we wouldn't normally use for testing
                tile_size=tile_size,
                pixels_per_fragment=pixels_per_fragment,
            )

            with rasterio.open(output_array) as src:
                self.assertEqual(src.bounds.left, expected_extents.minx)
                self.assertEqual(src.bounds.right, expected_extents.maxx)
                self.assertEqual(src.bounds.top, expected_extents.maxy)
                self.assertEqual(src.bounds.bottom, expected_extents.miny)
                self.assertEqual(src.profile["blockysize"], tile_size)
                self.assertEqual(src.profile["blockxsize"], tile_size)
                with rasterio.open(output_array) as src:
                    data = src.read(1, masked=True)
                    # all of test_1, 3/4 of test_2 and test_3 = 100 + 150 + 300
                    self.assertEqual(np.sum(data), 550)

            # check compression filter
            with tiledb.open(output_array) as src:
                fltr = src.schema.attr(0).filters[0]
                self.assertIsInstance(fltr, tiledb.ZstdFilter)
                self.assertEqual(fltr.level, 7)

    def test_raster_fragments(self):
        import rasterio

        import tiledb.cloud.geospatial as geo

        tile_size = 5
        # 25 pixels per tile, going to write at most 10 tiles per time
        # first two images overlap and form
        pixels_per_fragment = (tile_size**2) * 10
        test_1 = [self.test_dir.joinpath(r) for r in RASTER_NAMES[:3]]
        with mock.patch.object(VFS, "ls", return_value=test_1):
            output_array = str(self.test_dir.joinpath("frag_output_array"))
            # output_array = "/tmp/frag_output_array"

            # if os.path.exists(output_array):
            #     shutil.rmtree(output_array)

            dataset_list_uri = self.test_dir.joinpath("manifest.txt")
            with open(dataset_list_uri, "w") as f:
                for img in test_1:
                    f.write(f"{img}\n")

            run_local(
                dataset_uri=output_array,
                dataset_type=geo.DatasetType.RASTER,
                config={},
                dataset_list_uri=dataset_list_uri,
                nodata=255,
                # set batch size to 1 to test pixels_per_fragment
                batch_size=1,
                # pick a size we wouldn't normally use for testing
                tile_size=tile_size,
                pixels_per_fragment=pixels_per_fragment,
            )

            with rasterio.open(output_array) as src:
                # all of test_1, 3/4 of test_2 and test_3 = 100 + 150 + 300
                data = src.read(1, masked=True)
                self.assertEqual(np.sum(data), 550)

            # num_fragments
            fragments_info = tiledb.array_fragments(output_array)

            uris = geo.read_uris(dataset_list_uri, dataset_type=geo.DatasetType.RASTER)
            meta = geo.load_raster_metadata(uris)
            self.assertEqual(len(meta), 3)
            self.assertEqual(len(fragments_info), 8)

    def test_pointcloud_ingest(self):
        import tiledb.cloud.geospatial as geo

        test_1 = [self.test_dir.joinpath(r) for r in PC_NAMES]
        with mock.patch.object(VFS, "ls", return_value=test_1):
            output_array = str(self.test_dir.joinpath("pc_output_array"))
            dataset_list_uri = self.test_dir.joinpath("manifest.txt")
            with open(dataset_list_uri, "w") as f:
                for img in test_1:
                    f.write(f"{img}\n")

            run_local(
                dataset_uri=output_array,
                dataset_type=geo.DatasetType.POINTCLOUD,
                config={},
                dataset_list_uri=dataset_list_uri,
                batch_size=1,
                chunk_size=100,
            )

            with tiledb.open(output_array) as src:
                data = src[:]
                self.assertEqual(len(data["X"]), 1065)

    def test_geometry_ingest(self):
        import tiledb.cloud.geospatial as geo

        test_1 = [self.test_dir.joinpath(g) for g in GEOM_NAMES]
        with mock.patch.object(VFS, "ls", return_value=test_1):
            output_array = str(self.test_dir.joinpath("geom_output_array"))
            # output_array = "/tmp/geom_output_array"
            # if os.path.exists(output_array):
            #     shutil.rmtree(output_array)

            dataset_list_uri = self.test_dir.joinpath("manifest.txt")
            with open(dataset_list_uri, "w") as f:
                for g in test_1:
                    f.write(f"{g}\n")

            run_local(
                dataset_uri=output_array,
                dataset_type=geo.DatasetType.GEOMETRY,
                config={},
                dataset_list_uri=dataset_list_uri,
                batch_size=1,
            )

            with tiledb.open(output_array) as src:
                data = src[:]
                self.assertEqual(len(data["wkb_geometry"]), 3)

    def test_chunk(self):
        # chunking is critical, so lets include a test here
        samples = [self.test_dir.joinpath(r) for r in RASTER_NAMES[:3]]

        # Three nodes with 1 job are expected
        batch_size = 1
        result = utils.chunk(samples, batch_size)
        expected = 3
        self.assertEqual(len(tuple(result)), expected)

        # Two nodes with 2,1 jobs are expected
        batch_size = 2
        result = utils.chunk(samples, batch_size)
        expected = 2
        self.assertEqual(len(tuple(result)), expected)

        # One node with all jobs is expected
        batch_size = 3
        result = utils.chunk(samples, batch_size)
        expected = 1
        self.assertEqual(len(tuple(result)), expected)
