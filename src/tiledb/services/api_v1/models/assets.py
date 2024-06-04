from enum import Enum

from pydantic import BaseModel


class StorageLocation(BaseModel):
    path: str
    credentials_name: str


class AssetTypes(str, Enum):
    ARRAY = "array"
    NOTEBOOK = "notebook"
    DASHBOARD = "dashboard"
    USER_DEFINED_FUNCTION = "user_defined_function"
    ML_MODEL = "ml_model"
    FILE = "file"
    REGISTERED_TASK_GRAPH = "registered_task_graph"
    GROUP = "group"
    VCF = "vcf"
    SOMA = "soma"
    POINTCLOUD = "pointcloud"
    BIOIMG = "bioimg"
    GEOMETRY = "geometry"
    RASTER = "raster"
    VECTOR_SEARCH = "vector_search"


class AssetLocations(BaseModel):
    arrays: StorageLocation
    files: StorageLocation
    groups: StorageLocation
    ml_models: StorageLocation
    notebooks: StorageLocation
    task_graphs: StorageLocation
    udfs: StorageLocation
