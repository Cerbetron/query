"""Excel parsing utilities."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd

__all__ = ["load_resources_from_excel"]


_FIELDS = [
    "name",
    "description",
    "eligibility",
    "system",
    "service_type",
    "min_age",
    "max_age",
    "counties",
    "insurance_types",
    "partners",
    "tags",
]


def _as_list(value: Any) -> Optional[List[str]]:
    """Return a list of strings from a cell value."""

    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def _as_int(value: Any) -> Optional[int]:
    """Coerce a value to ``int`` when possible."""

    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize column names and values for a row."""

    normalized: Dict[str, Any] = {}
    for field in _FIELDS:
        val = row.get(field)
        if field in {"counties", "insurance_types", "partners", "tags"}:
            normalized[field] = _as_list(val)
        elif field in {"min_age", "max_age"}:
            normalized[field] = _as_int(val)
        else:
            if val is not None and not (isinstance(val, float) and pd.isna(val)):
                normalized[field] = str(val)
            else:
                normalized[field] = None
    return normalized


def load_resources_from_excel(path: str) -> List[Dict[str, Any]]:
    """Load and normalize resource information from an Excel workbook."""

    workbook = pd.ExcelFile(path)
    resources: List[Dict[str, Any]] = []
    for sheet in workbook.sheet_names[:10]:
        frame = pd.read_excel(workbook, sheet_name=sheet)
        frame.columns = [
            str(c).strip().lower().replace(" ", "_") for c in frame.columns
        ]
        for _, row in frame.iterrows():
            resources.append(_normalize_row(row.to_dict()))
    return resources
