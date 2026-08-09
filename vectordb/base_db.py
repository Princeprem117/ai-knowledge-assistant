from abc import ABC, abstractmethod
from typing import Any


class BaseVectorStore(ABC):
    """
    Abstract base class for vector store implementations.
    """

    @abstractmethod
    def add(
        self,
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        ids: list[str],
    ) -> None:
        """
        Add documents, embeddings, metadata, and IDs to the vector store.
        """
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Search for documents similar to the query embedding.
        """
        pass

    @abstractmethod
    def delete(self, ids: list[str]) -> None:
        """
        Delete documents from the vector store using their IDs.
        """
        pass