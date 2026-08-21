from embeddings.sentence_transformer import SentenceTransformerEmbedding
from rag.pipeline import RAGPipeline
from retrieval.context_builder import ContextBuilder
from retrieval.retriever import Retriever
from vectordb.chroma_db import ChromaVectorStore


class FakeLLM:

    def generate(
        self,
        prompt: str,
    ) -> str:
        return f"ANSWER:\n{prompt}"


def test_rag_pipeline():

    # 1. Create embedding model
    embedder = SentenceTransformerEmbedding()

    # 2. Create vector store
    store = ChromaVectorStore(
        persist_directory="data/test_rag"
    )

    # 3. Knowledge base
    documents = [
        "Python is a programming language.",
        "Java is used for enterprise applications.",
        "Python supports object-oriented programming.",
    ]

    ids = [
        "rag_python_001",
        "rag_java_001",
        "rag_python_002",
    ]

    metadatas = [
        {"source": "python.txt"},
        {"source": "java.txt"},
        {"source": "python.txt"},
    ]

    # 4. Generate embeddings
    embeddings = [
        embedder.embed(document)
        for document in documents
    ]

    # 5. Store knowledge
    store.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    # 6. Create retriever
    retriever = Retriever(
        embedding_model=embedder,
        vector_store=store,
    )

    # 7. Create context builder
    context_builder = ContextBuilder()

    # 8. Create LLM
    llm = FakeLLM()

    # 9. Create RAG pipeline
    rag = RAGPipeline(
        retriever=retriever,
        context_builder=context_builder,
        llm=llm,
    )

    # 10. Ask question
    answer = rag.ask(
        question="What is Python?",
        top_k=2,
    )

    print("\nRAG answer:")
    print(answer)

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0