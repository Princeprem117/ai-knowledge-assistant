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
        #getting the source ids
    @abstractmethod
    def get_ids_by_source(self, source: str) -> list[str]:
        """
        Return all chunk IDs belonging to a source document.
        """
        pass
    # list docs
    @abstractmethod
    def list_documents(self) -> list[dict[str, Any]]:
        """
        Return the documents currently stored in the vector store.
        """
        pass