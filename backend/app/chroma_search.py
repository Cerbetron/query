"""Utilities for embedding and searching resources with Chroma."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

import os

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

__all__ = ["index_resources", "search_chroma"]

# Default directory to persist the Chroma database
_CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")

# Initialize global model and Chroma collection
_model: SentenceTransformer | None = None
_collection: chromadb.api.types.Collection | None = None


def _get_collection() -> chromadb.api.types.Collection:
    """Return the Chroma collection, creating it if needed."""
    global _collection, _model
    if _collection is None:
        client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=_CHROMA_DIR))
        _collection = client.get_or_create_collection("resources")
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _collection


def index_resources(records: Iterable[Dict[str, Any]]) -> None:
    """Index ``records`` in Chroma."""
    collection = _get_collection()
    texts: List[str] = []
    metadatas: List[Dict[str, Any]] = []
    ids: List[str] = []
    for rec in records:
        text_parts = [rec.get("name") or "", rec.get("description") or "", rec.get("eligibility") or ""]
        text = "\n".join(part for part in text_parts if part).strip()
        if not text:
            # Skip records without textual content
            continue
        texts.append(text)
        metadatas.append({
            "id": rec.get("id"),
            "name": rec.get("name"),
            "system": rec.get("system"),
            "tags": rec.get("tags"),
        })
        ids.append(str(rec.get("id")))
    if not texts:
        return
    embeddings = _model.encode(texts).tolist()
    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    if hasattr(collection, "persist"):
        collection.persist()


def search_chroma(query: str) -> List[Dict[str, Any]]:
    """Return up to 5 resources from Chroma that best match ``query``."""
    if not query:
        return []
    collection = _get_collection()
    query_embedding = _model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    metadatas = results.get("metadatas", [[]])[0]
    return metadatas
