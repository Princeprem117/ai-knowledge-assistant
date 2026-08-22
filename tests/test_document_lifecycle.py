import pytest
from pathlib import Path
from unittest.mock import MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, DocumentRecord

from services.document_lifecycle_service import (
    DocumentLifecycleService,
)

from rag.service import RAGService
from rag.pipeline import RAGPipeline
from ingestion.service import DocumentIngestionService


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

    async def create(self, **kwargs):

        with self.session_factory() as session:

            document = DocumentRecord(**kwargs)

            session.add(document)

            session.commit()

            session.refresh(document)

            return document

    async def find_by_user_and_hash(
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

    async def update_status(
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


@pytest.mark.asyncio
async def test_duplicate_detection(tmp_path):

    # --------------------------------------------------
    # 1. Create test file
    # --------------------------------------------------

    file = tmp_path / "sample.txt"

    file.write_text(
        "hello world",
        encoding="utf-8",
    )

    # --------------------------------------------------
    # 2. Create isolated test database
    # --------------------------------------------------

    test_database = (
        tmp_path / "test_documents.db"
    )

    test_engine = create_engine(
        f"sqlite:///{test_database}",
    )

    Base.metadata.create_all(
        test_engine
    )

    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    # --------------------------------------------------
    # 3. Create repository
    # --------------------------------------------------

    repo = FakeDocumentRepository(
        session_factory=TestSessionLocal
    )

    # --------------------------------------------------
    # 4. Create lifecycle service
    # --------------------------------------------------

    lifecycle = DocumentLifecycleService(
        repository=repo,
        rag_service=FakeRAGService(),
    )

    # --------------------------------------------------
    # 5. First upload
    # --------------------------------------------------

    first = await lifecycle.upload_document(
        file_path=str(file),
        user_id="user1",
    )

    # --------------------------------------------------
    # 6. Second upload
    # --------------------------------------------------

    second = await lifecycle.upload_document(
        file_path=str(file),
        user_id="user1",
    )

    # --------------------------------------------------
    # 7. Validate duplicate detection
    # --------------------------------------------------

    assert first["duplicate"] is False

    assert second["duplicate"] is True

    assert first["chunks"] == 3

    assert second["chunks"] == 0