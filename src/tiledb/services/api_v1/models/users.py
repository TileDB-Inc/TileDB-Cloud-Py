from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    name: str
    email: str
    is_valid_email: bool
    stripe_connect: bool
    company: str
    logo: str
    timezone: str
    organizations: List[dict]
    allowed_actions: List[str]
    enabled_features: List[str]
    unpaid_subscription: bool
    default_s3_path: str
    default_s3_path_credentials_name: str
    asset_locations: Optional[dict] = None
    default_namespace_charged: str
    default_region: str
