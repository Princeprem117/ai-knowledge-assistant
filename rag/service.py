from ingestion.service import DocumentIngestionService
from rag.pipeline import RAGPipeline


class RAGService:
    """
    Application-level service that coordinates
    document ingestion and question answering.
    """

    def __init__(
        self,
        rag_pipeline: RAGPipeline,
        ingestion_service: DocumentIngestionService,
    ):
        self.rag_pipeline = rag_pipeline
        self.ingestion_service = ingestion_service

    def ingest_file(
        self,
        file_path: str,
    ) -> int:
        """
        Ingest a file into the knowledge base.
        """

        return self.ingestion_service.ingest_file(
            file_path
        )

    def ask(
        self,
        question: str,
        top_k: int = 3,
    ) -> str:
        """
        Ask a question against the knowledge base.
        """

        return self.rag_pipeline.ask(
            question=question,
            top_k=top_k,
        )