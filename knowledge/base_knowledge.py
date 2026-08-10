from ingestion.service import DocumentIngestionService
from retrieval.retriever import Retriever


class BaseKnowledge:

    def __init__(
        self,
        ingestion_service: DocumentIngestionService,
        retriever: Retriever,
    ):
        self.ingestion_service = ingestion_service
        self.retriever = retriever

    def ingest_file(self, file_path: str) -> int:
        """
        Add a file to the knowledge base.

        Returns the number of chunks stored.
        """

        return self.ingestion_service.ingest_file(
            file_path
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ):
        """
        Search the knowledge base for relevant documents.
        """

        return self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )