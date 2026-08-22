from fastapi import APIRouter

from app.dependencies import create_knowledge_base
from services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


# Create the application dependencies
rag_service, document_service , document_lifecycle_service = create_knowledge_base()


@router.get("/")
def list_documents():
    """
    Return all documents in the knowledge base.
    """

    return document_service.list_documents()


@router.delete("/{filename}")
def delete_document(filename: str):
    """
    Delete a document and all its chunks.
    """

    deleted_chunks = document_service.delete_document(
        filename
    )

    return {
        "filename": filename,
        "deleted_chunks": deleted_chunks,
    }