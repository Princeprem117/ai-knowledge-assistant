from pathlib import Path
from typing import Any

import chromadb

from vectordb.base_db import BaseVectorStore
class ChromaVectorStore(BaseVectorStore):
    """
    ChromaDB implementation of the vector store.
    """

    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "knowledge",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory
            )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
            )

    # ============================================================
    # Add / update documents
    # ============================================================

    def add(
        self,
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        ids: list[str],
    ) -> None:
        """
        Add or update documents in ChromaDB.

        Upsert is used because chunk IDs are deterministic.
        This prevents problems when the same document is
        ingested again.
        """

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    # ============================================================
    # Search
    # ============================================================

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Search for documents similar to the query embedding.
        """

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        return results

    # ============================================================
    # Delete
    # ============================================================

    def delete(
        self,
        ids: list[str],
    ) -> None:
        """
        Delete documents from ChromaDB using their IDs.
        """

        if not ids:
            return

        self.collection.delete(ids=ids)

    # ============================================================
    # Get IDs by source
    # ============================================================

    def get_ids_by_source(
        self,
        source: str,
    ) -> list[str]:
        """
        Return all chunk IDs belonging to a source document.

        Source matching is based on the filename so that both:

            IntelligentAgents_info.pdf

        and:

            C:/Python/AI Knowledge Assistant/data/uploads/IntelligentAgents_info.pdf

        are treated as the same document.
        """

        source_name = Path(source).name

        results = self.collection.get(
            include=["metadatas"],
        )

        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [])

        matching_ids = []

        for chunk_id, metadata in zip(
            ids,
            metadatas,
        ):
            stored_source = metadata.get(
                "source",
                "",
            )

            if Path(stored_source).name == source_name:
                matching_ids.append(chunk_id)

        return matching_ids

    # ============================================================
    # List documents
    # ============================================================

    def list_documents(
        self,
    ) -> list[dict[str, Any]]:
        """
        Return metadata for all stored chunks.
        """

        results = self.collection.get(
            include=[
                "metadatas"
            ],
        )

        return results.get(
            "metadatas",
            []
        )