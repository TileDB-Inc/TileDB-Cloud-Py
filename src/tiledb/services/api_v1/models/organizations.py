from enum import Enum
from typing import List

from pydantic import BaseModel

from tiledb.services.api_v1.models.namespaces import NamespaceActions


class OrganizationRoles(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    READ_WRITE = "read_write"
    READ_ONLY = "read_only"


class OrganizationUser(BaseModel):
    user_id: str
    organization_id: str
    username: str
    organization_name: str
    role: OrganizationRoles
    allowed_actions: List[NamespaceActions]
