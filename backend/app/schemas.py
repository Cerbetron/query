from typing import List, Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    """Shared attributes for resources excluding the database id."""

    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class ResourceOut(ResourceBase):
    """Representation of a resource returned by the API including the id."""

    id: int


class SearchRequest(BaseModel):
    """Payload accepted by the search API."""

    keyword: Optional[str] = None
    filters: Optional[List[str]] = None
