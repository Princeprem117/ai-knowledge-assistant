from models.document import Document
from ingestion.pipeline import IngestionPipeline


def test_document_identity_is_stable():
    document = Document(
        content="This is a test document.",
        metadata={
            "source": "test.pdf",
        },
    )

    first_id = IngestionPipeline._create_document_id(
        user_id="user_a",
        document=document,
    )

    second_id = IngestionPipeline._create_document_id(
        user_id="user_a",
        document=document,
    )

    assert first_id == second_id


def test_different_users_get_different_document_ids():
    document = Document(
        content="This is a test document.",
        metadata={
            "source": "test.pdf",
        },
    )

    user_a_id = IngestionPipeline._create_document_id(
        user_id="user_a",
        document=document,
    )

    user_b_id = IngestionPipeline._create_document_id(
        user_id="user_b",
        document=document,
    )

    assert user_a_id != user_b_id


def test_changed_content_gets_different_document_id():
    document_a = Document(
        content="Original content",
        metadata={
            "source": "test.pdf",
        },
    )

    document_b = Document(
        content="Changed content",
        metadata={
            "source": "test.pdf",
        },
    )

    document_a_id = IngestionPipeline._create_document_id(
        user_id="user_a",
        document=document_a,
    )

    document_b_id = IngestionPipeline._create_document_id(
        user_id="user_a",
        document=document_b,
    )

    assert document_a_id != document_b_id