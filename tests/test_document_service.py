from config import CHROMA_PERSIST_DIRECTORY

from services.document_service import DocumentService
from vectordb.chroma_db import ChromaVectorStore


def create_service():

    vector_store = ChromaVectorStore(
        persist_directory=CHROMA_PERSIST_DIRECTORY
    )

    return DocumentService(
        vector_store=vector_store
    )


def test_document_service():

    service = create_service()

    documents = service.list_documents()

    print("\n--- Documents ---")

    for document in documents:
        print(document)

    assert isinstance(documents, list)


def test_delete_document():

    service = create_service()

    documents_before = service.list_documents()

    print("\n--- Documents Before Delete ---")

    for document in documents_before:
        print(document)

    if not documents_before:
        print("\nNo documents available to delete.")
        return

    filename = documents_before[0]["filename"]

    print(f"\nDeleting: {filename}")

    deleted_chunks = service.delete_document(
        filename
    )

    print(
        f"Deleted chunks: {deleted_chunks}"
    )

    documents_after = service.list_documents()

    print("\n--- Documents After Delete ---")

    for document in documents_after:
        print(document)

    remaining_filenames = [
        document["filename"]
        for document in documents_after
    ]

    assert filename not in remaining_filenames