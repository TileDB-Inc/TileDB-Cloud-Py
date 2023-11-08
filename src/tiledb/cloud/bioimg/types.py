import enum
from dataclasses import dataclass

class EMBEDDINGS(enum.Enum):
    RESNET = enum.auto()

@dataclass
class SupportedExtensions:
    TIFF: str = ".tiff"
    TIF: str = ".tif"
    SVS: str = ".svs"
    TDB: str = ".tdb"