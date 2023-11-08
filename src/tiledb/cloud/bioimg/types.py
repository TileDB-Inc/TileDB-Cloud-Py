import enum

class EMBEDDINGS(enum.Enum):
    RESNET = enum.auto()

class SupportedExtensions(enum.Enum):
    TIFF: str = ".tiff"
    TIF: str = ".tif"
    SVS: str = ".svs"
    TDB: str = ".tdb"