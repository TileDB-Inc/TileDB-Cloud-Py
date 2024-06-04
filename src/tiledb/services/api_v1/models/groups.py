from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GroupUpdateInfo:
    description: Optional[str]
    name: Optional[str]
    logo: Optional[str]
    tags: Optional[List[str]]
