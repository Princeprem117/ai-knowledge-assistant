import chromadb

from vectordb.base_db import BaseVectorStore


class ChromaVectorStore(BaseVectorStore):
    """ChromaDB implementation of the vector store."""

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

    def add(
        self,
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
        ids: list[str],
    ) -> None:
        """Add documents and their embeddings to ChromaDB."""

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict:
        """Search for documents similar to the query embedding."""

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        return results

    def delete(self, ids: list[str]) -> None:
        """Delete documents from ChromaDB using their IDs."""

        self.collection.delete(
            ids=ids
        )