from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas import SearchRequest, ResourceOut

router = APIRouter()

# Demo data for example purposes
_demo_resources: List[ResourceOut] = [
    ResourceOut(
        id=1,
        name="Resource One",
        url="https://example.com/1",
        description="First example resource",
        tags=["example", "demo"],
    ),
    ResourceOut(
        id=2,
        name="Resource Two",
        url="https://example.com/2",
        description="Second example resource",
        tags=["sample"],
    ),
    ResourceOut(
        id=3,
        name="Resource Three",
        url="https://example.com/3",
        description="Third example resource",
        tags=["demo"],
    ),
    ResourceOut(
        id=4,
        name="Resource Four",
        url="https://example.com/4",
        description="Fourth example resource",
        tags=["demo", "test"],
    ),
    ResourceOut(
        id=5,
        name="Resource Five",
        url="https://example.com/5",
        description="Fifth example resource",
        tags=["example"],
    ),
]


@router.post("/search", response_model=List[ResourceOut])
async def search_resources(payload: SearchRequest) -> List[ResourceOut]:
    """Simple search over demo data."""
    results = _demo_resources
    if payload.keyword:
        keyword = payload.keyword.lower()
        results = [
            r
            for r in results
            if keyword in r.name.lower()
            or (r.description and keyword in r.description.lower())
        ]
    if payload.filters:
        results = [
            r
            for r in results
            if r.tags and any(tag in payload.filters for tag in r.tags)
        ]
    return results


@router.get("/details/{resource_id}", response_model=ResourceOut)
async def get_resource(resource_id: int) -> ResourceOut:
    """Return a resource by id from the demo dataset."""
    for res in _demo_resources:
        if res.id == resource_id:
            return res
    raise HTTPException(status_code=404, detail="Resource not found")


@router.get("/demo", response_model=List[ResourceOut])
async def demo_resources() -> List[ResourceOut]:
    """Return hardcoded demo resources."""
    return _demo_resources
