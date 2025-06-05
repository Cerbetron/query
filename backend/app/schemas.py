from typing import List, Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    """Shared attributes for resources."""

    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    eligibility: Optional[str] = None
    service_type: Optional[str] = None
    system: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    counties: Optional[List[str]] = None
    insurance_types: Optional[List[str]] = None
    partners: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class ResourceOut(ResourceBase):
    """Representation of a resource returned by the API including the id."""

    id: int


class SearchRequest(BaseModel):
    """Payload accepted by the search API."""

    keyword: Optional[str] = None
    age: Optional[int] = None
    county: Optional[str] = None
    insurance: Optional[str] = None
    system: Optional[List[str]] = None
    tags: Optional[List[str]] = None
