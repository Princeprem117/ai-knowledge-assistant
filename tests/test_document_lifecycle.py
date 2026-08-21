from unittest.mock import MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rag.pipeline import RAGPipeline
from rag.service import RAGService
from ingestion.service import DocumentIngestionService

from database.models import Base, DocumentRecord

from services.document_lifecycle_service import (
    DocumentLifecycleService,
)


class FakeRAGService(RAGService):

    def __init__(self):
        super().__init__(
            rag_pipeline=MagicMock(spec=RAGPipeline),
            ingestion_service=MagicMock(
                spec=DocumentIngestionService
            ),
        )

    def ingest_file(
        self,
        file_path,
        user_id,
    ):
        return 3


class FakeDocumentRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create(self, **kwargs):

        with self.session_factory() as session:

            document = DocumentRecord(**kwargs)

            session.add(document)

            session.commit()

            session.refresh(document)

            return document

    def find_by_user_and_hash(
        self,
        user_id: str,
        content_hash: str,
    ):

        with self.session_factory() as session:

            return (
                session.query(DocumentRecord)
                .filter(
                    DocumentRecord.user_id == user_id,
                    DocumentRecord.content_hash == content_hash,
                )
                .first()
            )

    def update_status(
        self,
        document_id: str,
        status: str,
    ):

        with self.session_factory() as session:

            document = (
                session.query(DocumentRecord)
                .filter(
                    DocumentRecord.id == document_id
                )
                .first()
            )

            if document:
                document.processing_status = status
                session.commit()


def test_duplicate_detection(tmp_path):

    file = tmp_path / "sample.txt"

    file.write_text(
        "hello world",
        encoding="utf-8",
    )

    # ---------------------------------------------
    # Isolated test database
    # ---------------------------------------------

    test_database = tmp_path / "test_documents.db"

    test_engine = create_engine(
        f"sqlite:///{test_database}",
    )

    Base.metadata.create_all(test_engine)

    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    # ---------------------------------------------
    # Test repository
    # ---------------------------------------------

    repo = FakeDocumentRepository(
        session_factory=TestSessionLocal
    )

    lifecycle = DocumentLifecycleService(
        repository=repo,
        rag_service=FakeRAGService(),
    )

    # ---------------------------------------------
    # First upload
    # ---------------------------------------------

    first = lifecycle.upload_document(
        file_path=str(file),
        user_id="user1",
    )

    # ---------------------------------------------
    # Second upload
    # ---------------------------------------------

    second = lifecycle.upload_document(
        file_path=str(file),
        user_id="user1",
    )

    # ---------------------------------------------
    # Assertions
    # ---------------------------------------------

    assert first["duplicate"] is False

    assert second["duplicate"] is True