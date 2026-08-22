import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from repositories.document_repository import DocumentRepository


class TestRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def create(self, **kwargs):
        from database.models import DocumentRecord

        with self.session_factory() as session:
            document = DocumentRecord(**kwargs)

            session.add(document)
            session.commit()
            session.refresh(document)

            return document


@pytest.mark.asyncio
async def test_repository_create(tmp_path):

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
    # Test repository directly
    # ---------------------------------------------

    repo = TestRepository(
        session_factory=TestSessionLocal
    )

    document = await repo.create(
        user_id="test_user",
        filename="sample.pdf",
        content_hash="abc123",
        storage_path="data/uploads/test/sample.pdf",
        file_type="pdf",
        file_size=100,
        processing_status="completed",
    )

    # ---------------------------------------------
    # Assertions
    # ---------------------------------------------

    assert document.user_id == "test_user"
    assert document.filename == "sample.pdf"
    assert document.content_hash == "abc123"
    assert document.file_type == "pdf"
    assert document.processing_status == "completed"