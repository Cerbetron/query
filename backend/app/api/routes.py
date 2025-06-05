from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas import SearchRequest, ResourceOut
from app.chroma_search import index_resources, search_chroma

router = APIRouter()

# Demo data for example purposes
_demo_resources: List[ResourceOut] = [
    ResourceOut(
        id=1,
        name="Resource One",
        url="https://example.com/1",
        description="First example resource",
        eligibility="Teens in Alameda",
        service_type="outpatient",
        system="Education",
        min_age=13,
        max_age=18,
        counties=["Alameda"],
        insurance_types=["Private"],
        partners=["Partner A"],
        tags=["example", "demo"],
    ),
    ResourceOut(
        id=2,
        name="Resource Two",
        url="https://example.com/2",
        description="Second example resource",
        eligibility="Adults in Contra Costa",
        service_type="residential",
        system="Healthcare",
        min_age=18,
        counties=["Contra Costa"],
        insurance_types=["Medicaid"],
        partners=["Partner B"],
        tags=["sample"],
    ),
    ResourceOut(
        id=3,
        name="Resource Three",
        url="https://example.com/3",
        description="Third example resource",
        eligibility="Youth drop in",
        service_type="drop-in",
        system="Housing",
        max_age=25,
        counties=["Alameda"],
        insurance_types=["None"],
        partners=["Partner C"],
        tags=["demo"],
    ),
    ResourceOut(
        id=4,
        name="Resource Four",
        url="https://example.com/4",
        description="Fourth example resource",
        eligibility="Bilingual therapy",
        system="Healthcare",
        counties=["San Francisco"],
        insurance_types=["Private"],
        partners=["Partner D"],
        tags=["demo", "test"],
    ),
    ResourceOut(
        id=5,
        name="Resource Five",
        url="https://example.com/5",
        description="Fifth example resource",
        eligibility="Support groups",
        service_type="support",
        counties=["Alameda"],
        insurance_types=["Medicaid"],
        partners=["Partner E"],
        tags=["example"],
    ),
]

# Index demo resources into Chroma on startup
index_resources([r.model_dump() for r in _demo_resources])


@router.post("/search", response_model=List[ResourceOut])
async def search_resources(payload: SearchRequest) -> List[ResourceOut]:
    """Simple search over demo data using multiple filters."""
    results = _demo_resources
    if payload.keyword:
        keyword = payload.keyword.lower()
        results = [
            r
            for r in results
            if keyword in r.name.lower()
            or (r.description and keyword in r.description.lower())
            or (r.eligibility and keyword in r.eligibility.lower())
        ]
        vector_ids = [int(m.get("id")) for m in search_chroma(payload.keyword) if m.get("id")]
        if vector_ids:
            order = {rid: idx for idx, rid in enumerate(vector_ids)}
            results.sort(key=lambda r: order.get(r.id, len(order)))
    if payload.tags:
        results = [
            r
            for r in results
            if r.tags and any(tag in payload.tags for tag in r.tags)
        ]
    if payload.age is not None:
        results = [
            r
            for r in results
            if (
                (r.min_age is None or r.min_age <= payload.age)
                and (r.max_age is None or payload.age <= r.max_age)
            )
        ]
    if payload.county:
        results = [
            r
            for r in results
            if r.counties and payload.county in r.counties
        ]
    if payload.insurance:
        results = [
            r
            for r in results
            if r.insurance_types and payload.insurance in r.insurance_types
        ]
    if payload.system:
        results = [
            r for r in results if r.system and r.system in payload.system
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
