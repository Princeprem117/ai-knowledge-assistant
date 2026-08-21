from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, DocumentRecord
from repositories.document_repository import DocumentRepository


def test_repository_create(tmp_path):
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
    # Temporarily replace the repository's
    # SessionLocal with the isolated test session
    # ---------------------------------------------

    import repositories.document_repository as repository_module

    original_session_local = repository_module.SessionLocal

    repository_module.SessionLocal = TestSessionLocal

    try:

        repo = DocumentRepository()

        document = repo.create(

            user_id="test_user",

            filename="sample.pdf",

            content_hash="abc123",

            storage_path="data/uploads/test/sample.pdf",

            file_type="pdf",

            file_size=100,

            processing_status="completed",
        )

        assert document.user_id == "test_user"

        assert document.filename == "sample.pdf"

        assert document.content_hash == "abc123"

    finally:

        repository_module.SessionLocal = original_session_local