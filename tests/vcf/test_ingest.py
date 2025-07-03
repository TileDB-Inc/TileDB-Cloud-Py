import io
import logging
import re
import unittest
from contextlib import redirect_stdout

import tiledbvcf

import tiledb.cloud
import tiledb.cloud.vcf
from tiledb.cloud._vendor import cloudpickle
from tiledb.cloud.utilities import get_logger

# Pickle the vcf module by value, so tests run on the latest code.
cloudpickle.register_pickle_by_value(tiledb.cloud.vcf)

# Test data location
S3_BUCKET = "s3://tiledb-unittest/vcf-ingestion-test"

# Test VCF URIs
READY_URI = f"{S3_BUCKET}/01-ready.vcf.gz"  # "OK" after ingestion
MISSING_INDEX_URI = f"{S3_BUCKET}/02-missing-index.vcf.gz"  # "OK" after ingestion
MISSING_SAMPLE_NAME_URI = f"{S3_BUCKET}/03-missing-sample-name.vcf.gz"
MULTIPLE_SAMPLES_URI = f"{S3_BUCKET}/04-multiple-samples.vcf.gz"
DUPLICATE_SAMPLE_NAME_URI = f"{S3_BUCKET}/05-duplicate-sample-name.vcf.gz"
BAD_INDEX_URI = f"{S3_BUCKET}/06-bad-index.vcf.gz"

# Test data samples
READY_SAMPLE_NAME = "ready"
MISSING_INDEX_SAMPLE_NAME = "missing index"

# Array names
LOG_ARRAY = "log"
MANIFEST_ARRAY = "manifest"

# Filter samples log message
FILTER_SAMPLES_LOG = (
    "Filtering samples: "
    "len(dataset_samples)={}, "
    "len(ingested_samples)={}, "
    "len(incomplete_samples)={}, "
    "len(manifest_samples)={}, "
    "len(ready_samples)={}, "
    "len(queued_samples)={}"
)


def outputs2msgs(outputs: list[str]) -> list[str]:
    """
    Extracts the messages from log outputs with the format
    "[%(asctime)s] [%(module)s] [%(funcName)s] [%(levelname)s] %(message)s"
    """
    pattern = re.compile(r"\[.*\] \[.*\] \[.*\] \[.*\] ")
    msgs = []
    for o in outputs:
        if pattern.match(o):
            msg = pattern.sub("", o)
            msgs.append(msg)
        else:
            msgs.append(o)
    return msgs


class TestVCFIngestionBase(unittest.TestCase):
    __unittest_skip__ = True

    @classmethod
    def _setup(cls) -> None:
        cls.data_uri = S3_BUCKET
        (
            cls.namespace,
            cls.storage_path,
            cls.acn,
        ) = tiledb.cloud.groups._default_ns_path_cred()
        cls.namespace = cls.namespace.rstrip("/")
        cls.storage_path = cls.storage_path.rstrip("/")
        cls.array_name = tiledb.cloud._common.testonly.random_name("vcf-test")
        cls.dataset_uri = (
            f"tiledb://{cls.namespace}/{cls.storage_path}/{cls.array_name}"
        )

    @classmethod
    def _ingest(cls) -> None:
        raise NotImplementedError("Implement VCF ingestion")

    @classmethod
    def setUpClass(cls) -> None:
        cls._setup()

        # Capture local and cloud logs during ingestion
        logger = get_logger(logging.INFO)
        f = io.StringIO()  # cloud logs are printed
        with cls.assertLogs(cls, logger=logger) as lg, redirect_stdout(f):
            cls._ingest()
        local_logs = list(map(lambda r: r.getMessage(), lg.records))
        cloud_logs = outputs2msgs(f.getvalue().splitlines())
        cls.logs = local_logs + cloud_logs

    @classmethod
    def tearDownClass(cls) -> None:
        if tiledb.object_type(cls.dataset_uri):
            tiledb.cloud.asset.delete(cls.dataset_uri, recursive=True)

    def test_dataset_creation(self):
        self.assertIn(f"Creating dataset: dataset_uri='{self.dataset_uri}'", self.logs)

    def test_dataset_group_and_arrays(self):
        self.assertEqual(tiledb.object_type(self.dataset_uri), "group")
        group = tiledb.Group(self.dataset_uri)
        manifest_uri = group[MANIFEST_ARRAY].uri
        self.assertEqual(tiledb.object_type(manifest_uri), "array")
        self.assertEqual(tiledb.object_type(group[LOG_ARRAY].uri), "array")

    def test_filter_uris(self):
        self.assertIn(
            "Filtering URIs: len(manifest_uris)=0, len(new_uris)=6", self.logs
        )

    def test_filter_samples(self):
        self.assertIn(FILTER_SAMPLES_LOG.format(0, 0, 0, 5, 2, 2), self.logs)

    def test_manifest(self):
        group = tiledb.Group(self.dataset_uri)
        manifest_uri = group[MANIFEST_ARRAY].uri
        with tiledb.open(manifest_uri) as A:
            manifest_df = A.df[:]

        ok_df = manifest_df[manifest_df["status"] == "ok"]
        self.assertEqual(len(ok_df), 2)
        self.assertIn(READY_URI, ok_df["vcf_uri"].tolist())
        self.assertIn(READY_URI + ".tbi", ok_df["index_uri"].tolist())
        self.assertIn(MISSING_INDEX_URI, ok_df["vcf_uri"].tolist())
        self.assertIn("None", ok_df["index_uri"].tolist())

        # NOTE: This code path is currently unreachable; an error is logged instead
        self.assertIn(
            f"Skipping invalid VCF file: vcf_uri='{MISSING_SAMPLE_NAME_URI}'", self.logs
        )

        multiple_samples_df = manifest_df[manifest_df["status"] == "multiple samples"]
        self.assertEqual(len(multiple_samples_df), 1)

        duplicate_sample_name_df = manifest_df[
            manifest_df["status"] == "duplicate sample name"
        ]
        self.assertEqual(len(duplicate_sample_name_df), 1)

        bad_index_df = manifest_df[manifest_df["status"] == "bad index"]
        self.assertEqual(len(bad_index_df), 1)

    def test_dataset(self):
        ds = tiledbvcf.Dataset(
            self.dataset_uri,
            cfg=tiledbvcf.ReadConfig(tiledb_config=self.config),
        )
        samples = ds.samples()
        self.assertEqual(len(samples), 2)
        self.assertIn(READY_SAMPLE_NAME, samples)
        self.assertIn(MISSING_INDEX_SAMPLE_NAME, samples)


class TestVCFIngestionSearch(TestVCFIngestionBase):
    __unittest_skip__ = False

    @classmethod
    def _setup(cls):
        super(TestVCFIngestionSearch, cls)._setup()
        cls.search_uri = cls.data_uri + "/"
        cls.search_pattern = "*.vcf.gz"

    @classmethod
    def _ingest(cls) -> None:
        tiledb.cloud.vcf.ingest_vcf(
            dataset_uri=cls.dataset_uri,
            search_uri=cls.search_uri,
            pattern=cls.search_pattern,
            config=cls.config,
            wait=True,
        )

    def test_find_uris_logs(self):
        msg = (
            "Searching for VCF URIs: "
            f"search_uri='{self.search_uri}', "
            f"include='{self.search_pattern}', "
            "exclude=None, "
            "len(vcf_uris)=6"
        )
        self.assertIn(msg, self.logs)


# TODO: sample_list_uri, disable_manifest

# TODO: metadata_uri, metadata_attr

# TODO: test resume
