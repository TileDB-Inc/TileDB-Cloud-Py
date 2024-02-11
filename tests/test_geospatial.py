import os
import shutil
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock

import affine
import numpy as np
import pdal
import rasterio

import tiledb
from tiledb.cloud.geospatial import BoundingBox
from tiledb.cloud.geospatial import get_raster_metadata
from tiledb.cloud.geospatial import ingest_datasets
from tiledb.cloud.utilities import batch
from tiledb.cloud.utilities import serialize_filter
from tiledb.vfs import VFS

RASTER_NAMES = [
    "test1.tif",
    "test2.tif",
    "test3.tif",
    "test_diff_res.tif",
    "test_diff_crs.tif",
]
PC_NAMES = ["test1.las", "test2.las", "test3.las"]


class GeospatialTest(unittest.TestCase):
    def setUp(self):
        # Ignore warnings
        warnings.simplefilter("ignore")
        # Create a temporary directory
        self.test_dir = Path(tempfile.mkdtemp())

        def create_test_rasters(tmp_path: os.PathLike):
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
            with rasterio.open(
                tmp_path.joinpath(RASTER_NAMES[0]), "w", **kwargs
            ) as dst:
                data = np.ones((10, 10), dtype=rasterio.uint8)
                dst.write(data, indexes=1)

            kwargs["transform"] = affine.Affine(0.2, 0, -113, 0, -0.2, 45)

            with rasterio.open(
                tmp_path.joinpath(RASTER_NAMES[1]), "w", **kwargs
            ) as dst:
                data = np.ones((10, 10), dtype=rasterio.uint8) * 2
                data[:5, :5] = 0
                dst.write(data, indexes=1)

            # distinct from test1 and test2 above
            kwargs["transform"] = affine.Affine(0.2, 0, -100, 0, -0.2, 35)

            with rasterio.open(
                tmp_path.joinpath(RASTER_NAMES[2]), "w", **kwargs
            ) as dst:
                data = np.ones((10, 10), dtype=rasterio.uint8) * 3
                dst.write(data, indexes=1)

            # write a different resolution
            kwargs["transform"] = affine.Affine(0.3, 0, -100, 0, -0.3, 35)
            with rasterio.open(
                tmp_path.joinpath(RASTER_NAMES[3]), "w", **kwargs
            ) as dst:
                data = np.ones((10, 10), dtype=rasterio.uint8) * 3
                dst.write(data, indexes=1)

            # write a different crs
            kwargs["crs"] = "EPSG:3857"
            kwargs["transform"] = affine.Affine(0.2, 0, 1000, 0, -0.2, 1000)
            with rasterio.open(
                tmp_path.joinpath(RASTER_NAMES[4]), "w", **kwargs
            ) as dst:
                data = np.ones((10, 10), dtype=rasterio.uint8) * 4
                dst.write(data, indexes=1)

        def create_point_clouds(tmp_path: os.PathLike):
            for i in range(1, 4):
                vals = [(i, i, i)]
                data = np.array(vals, dtype=[("X", float), ("Y", float), ("Z", float)])
                pipeline = pdal.Pipeline(arrays=[data]) | pdal.Writer.las(
                    filename=os.path.abspath(tmp_path.joinpath(f"test{i}.las"))
                )
                pipeline.execute()

        create_test_rasters(self.test_dir)
        create_point_clouds(self.test_dir)

        for r in RASTER_NAMES:
            self.assertTrue(os.path.exists(self.test_dir.joinpath(r)))

        for p in PC_NAMES:
            self.assertTrue(os.path.exists(self.test_dir.joinpath(p)))

        self.out_path = "out"

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_raster_get_metadata(self):
        tile_size = 16
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
            meta_1 = get_raster_metadata(test_1, dst_tile_size=tile_size)
            expected_extents = BoundingBox(minx=-114, miny=33, maxx=-98, maxy=46)
            self.assertEqual(meta_1.extents, expected_extents)
            self.assertEqual(len(meta_1.block_metadata), 3)
            self.assertEqual(len(meta_1.block_metadata[0].files), 2)
            self.assertEqual(meta_1.res, (0.2, 0.2))

            # test the first return value for the first block
            self.assertEqual(meta_1.block_metadata[0].files[0], test_1[0])

        # Case 1-2 Ingestion - Empty input list
        with mock.patch.object(VFS, "ls", return_value=ingest_uri_sample["test2"]):
            # Empty input list raises error
            with self.assertRaises(ValueError):
                get_raster_metadata(ingest_uri_sample["test2"])

        # Case 1-3 Ingestion - See if mixed resolutions are detected
        with mock.patch.object(VFS, "ls", return_value=ingest_uri_sample["test3"]):
            # Mixed resolutions without forcing target resolution raises error
            with self.assertRaises(ValueError):
                get_raster_metadata(ingest_uri_sample["test3"])

            tgt_res = (0.4, 0.4)
            meta_3 = get_raster_metadata(ingest_uri_sample["test3"], res=tgt_res)
            self.assertEqual(meta_3.res, tgt_res)

        # Case 1-4 Ingestion - See if mixed CRSs are detected
        # Same logic for data types and band counts
        with mock.patch.object(VFS, "ls", return_value=ingest_uri_sample["test4"]):
            # Mixed CRSs raises error
            with self.assertRaises(ValueError):
                get_raster_metadata(ingest_uri_sample["test4"])

        # TODO add tests for mixed band counts and data types

    def test_pointcloud_get_metadata(self):
        pass

    def test_geometry_get_metadata(self):
        pass

    def test_raster_ingest(self):
        tile_size = 16
        zstd_filter = tiledb.ZstdFilter(level=7)
        test_1 = [self.test_dir.joinpath(r) for r in RASTER_NAMES[:3]]
        meta_1 = get_raster_metadata(test_1, dst_tile_size=tile_size)
        self.assertEqual(len(meta_1.block_metadata), 3)
        output_array = str(self.test_dir.joinpath("raster_output_array"))
        dataset_list_uri = self.test_dir.joinpath("manifest.txt")
        with open(dataset_list_uri, "w") as f:
            for img in test_1:
                f.write(f"{img}\n")

        ingest_datasets(
            dataset_uri=output_array,
            dataset_type="raster",
            config={},
            dataset_list_uri=dataset_list_uri,
            compression_filter=serialize_filter(zstd_filter),
            # set batch size to 1 to test overlapping images
            batch_size=1,
            # pick a size we wouldn't normally use for testing
            tile_size=tile_size,
            unit_testing=True,
        )
        with rasterio.open(output_array) as src:
            self.assertEqual(src.bounds.left, meta_1.extents.minx)
            self.assertEqual(src.bounds.right, meta_1.extents.maxx)
            self.assertEqual(src.bounds.top, meta_1.extents.maxy)
            self.assertEqual(src.bounds.bottom, meta_1.extents.miny)
            self.assertEqual(src.profile["blockysize"], tile_size)
            self.assertEqual(src.profile["blockxsize"], tile_size)
            self.assertEqual(src.checksum(1), 57947)

        # check compression filter
        with tiledb.open(output_array) as src:
            fltr = src.schema.attr(0).filters[0]
            self.assertIsInstance(fltr, tiledb.ZstdFilter)
            self.assertEqual(fltr.level, 7)

    def test_point_cloud_ingest(self):
        pass

    def test_geometry_ingest(self):
        pass

    def test_batch(self):
        # batching is critical, so lets include a test here
        samples = [self.test_dir.joinpath(r) for r in RASTER_NAMES[:3]]

        # Three nodes with 1 job are expected
        batch_size = 1
        result = batch(samples, batch_size)
        expected = 3
        self.assertEqual(len(tuple(result)), expected)

        # Two nodes with 2,1 jobs are expected
        batch_size = 2
        result = batch(samples, batch_size)
        expected = 2
        self.assertEqual(len(tuple(result)), expected)

        # One node with all jobs is expected
        batch_size = 3
        result = batch(samples, batch_size)
        expected = 1
        self.assertEqual(len(tuple(result)), expected)
