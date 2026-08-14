from ingestion.service import DocumentIngestionService
from retrieval.retriever import Retriever
from pathlib import Path

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

        Prevent duplicate documents from being ingested.
        """

        if self.document_exists(file_path):
            raise ValueError(
                "Document already exists in the knowledge base."
            )

        return self.ingestion_service.ingest_file(
            file_path
            )
    # serching the User Query relevent Docs
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

    # To list the Docs
    def list_documents(self) -> list[dict]:

        """ List documents currently stored in the knowledge base."""

        return self.retriever.vector_store.list_documents()

    #  To Remove Documents
    def remove_document(self, file_path: str) -> int:
        """
        Remove all chunks belonging to a document.

        The vector database stores only the original
        filename as the source metadata.

        Returns the number of chunks removed.
        """

        source = Path(file_path).name

        ids = self.retriever.vector_store.get_ids_by_source(
            source
        )

        if not ids:
            return 0

        self.retriever.vector_store.delete(ids)

        return len(ids)


    # checks the doc is exists or not
    def document_exists(self, file_path: str) -> bool:
        """
        Check whether a document already exists
        in the knowledge base.
        """
        vector_store = getattr(self.retriever, "vector_store", None)
        if vector_store is None:
            return False
        ids = vector_store.get_ids_by_source(
        file_path)

        return bool(ids)