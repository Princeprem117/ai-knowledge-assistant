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


def test_rag_quality():

    # --------------------------------------------------
    # 1. Components
    # --------------------------------------------------

    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory="data/test_rag_quality"
    )

    # --------------------------------------------------
    # 2. Knowledge base
    # --------------------------------------------------

    documents = [
        "Python is a programming language.",
        "Python supports object-oriented programming.",
        "Java is commonly used for enterprise applications.",
    ]

    ids = [
        "quality_python_001",
        "quality_python_002",
        "quality_java_001",
    ]

    metadatas = [
        {"source": "python.txt"},
        {"source": "python.txt"},
        {"source": "java.txt"},
    ]

    # --------------------------------------------------
    # 3. Generate embeddings
    # --------------------------------------------------

    embeddings = [
        embedder.embed(document)
        for document in documents
    ]

    # --------------------------------------------------
    # 4. Store documents
    # --------------------------------------------------

    store.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    # --------------------------------------------------
    # 5. Create RAG components
    # --------------------------------------------------

    retriever = Retriever(
        embedding_model=embedder,
        vector_store=store,
    )

    context_builder = ContextBuilder()

    llm = FakeLLM()

    rag = RAGPipeline(
        retriever=retriever,
        context_builder=context_builder,
        llm=llm,
        relevance_threshold=1.0,
    )

    # --------------------------------------------------
    # 6. Test document-based question
    # --------------------------------------------------

    print("\n==============================")
    print("TEST 1: Document Question")
    print("==============================")

    answer = rag.ask(
        question="What is Python?",
        top_k=2,
    )

    print("\nAnswer:")
    print(answer)

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

    assert "Sources:" in answer

    # --------------------------------------------------
    # 7. Test another document question
    # --------------------------------------------------

    print("\n==============================")
    print("TEST 2: Java Question")
    print("==============================")

    answer = rag.ask(
        question="What is Java used for?",
        top_k=2,
    )

    print("\nAnswer:")
    print(answer)

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

    # --------------------------------------------------
    # 8. Test unrelated question
    # --------------------------------------------------

    print("\n==============================")
    print("TEST 3: Unrelated Question")
    print("==============================")

    answer = rag.ask(
        question="What is the capital of France?",
        top_k=2,
    )

    print("\nAnswer:")
    print(answer)

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

    assert (
        "couldn't find information"
        in answer.lower()
    )

    assert "Sources:" not in answer