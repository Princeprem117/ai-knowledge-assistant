from vectordb.chroma_db import ChromaVectorStore


def test_users_cannot_delete_each_others_documents(tmp_path):
    store = ChromaVectorStore(
        persist_directory=str(tmp_path / "chroma"),
        collection_name="test_documents",
    )

    store.add(
        documents=[
            "User A private document",
            "User B private document",
        ],
        embeddings=[
            [1.0, 0.0],
            [0.0, 1.0],
        ],
        metadatas=[
            {
                "user_id": "user_a",
                "filename": "agents.pdf",
                "source": "agents.pdf",
                "type": "pdf",
            },
            {
                "user_id": "user_b",
                "filename": "agents.pdf",
                "source": "agents.pdf",
                "type": "pdf",
            },
        ],
        ids=[
            "user_a_agents_chunk_000",
            "user_b_agents_chunk_000",
        ],
    )

    # User B searches for agents.pdf.
    # Only User B's chunk should be returned.
    user_b_ids = store.get_ids_by_source(
        "agents.pdf",
        user_id="user_b",
    )

    assert user_b_ids == [
        "user_b_agents_chunk_000"
    ]

    # User B deletes the IDs returned for their own document.
    store.delete(user_b_ids)

    # User A's document must still exist.
    user_a_ids = store.get_ids_by_source(
        "agents.pdf",
        user_id="user_a",
    )

    assert user_a_ids == [
        "user_a_agents_chunk_000"
    ]

    # User B's document must be gone.
    user_b_ids_after_delete = store.get_ids_by_source(
        "agents.pdf",
        user_id="user_b",
    )

    assert user_b_ids_after_delete == []