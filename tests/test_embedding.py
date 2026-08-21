from embeddings.sentence_transformer import SentenceTransformerEmbedding


def test_real_embedding_generation():
    embedder = SentenceTransformerEmbedding()

    text = "Python is a programming language."

    embedding = embedder.embed(text)

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(value, float) for value in embedding)

    print("Embedding dimension:", len(embedding))
    print("First 5 values:", embedding[:5])
