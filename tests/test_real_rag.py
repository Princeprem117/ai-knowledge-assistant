from pathlib import Path

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding
from ingestion.pipeline import IngestionPipeline
from models.document import Document
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


def test_real_document_rag():

    # --------------------------------------------------
    # 1. Load a real file
    # --------------------------------------------------

    file_path = Path("data/sample.txt")

    content = file_path.read_text(
        encoding="utf-8"
    )

    document = Document(
        content=content,
        metadata={
            "source": str(file_path)
        },
    )

    # --------------------------------------------------
    # 2. Create shared components
    # --------------------------------------------------

    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory="data/test_real_rag"
    )

    chunker = RecursiveChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    # --------------------------------------------------
    # 3. Ingest the document
    # --------------------------------------------------

    ingestion = IngestionPipeline(
        chunker=chunker,
        embedding_model=embedder,
        vector_store=store,
    )

    chunk_count = ingestion.ingest(
        [document],
        user_id="test_user",
    )

    print("\nChunks ingested:", chunk_count)

    assert chunk_count > 0

    # --------------------------------------------------
    # 4. Create retrieval components
    # --------------------------------------------------

    retriever = Retriever(
        embedding_model=embedder,
        vector_store=store,
    )

    context_builder = ContextBuilder()

    # --------------------------------------------------
    # 5. Create fake LLM
    # --------------------------------------------------

    llm = FakeLLM()

    # --------------------------------------------------
    # 6. Create RAG pipeline
    # --------------------------------------------------

    rag = RAGPipeline(
        retriever=retriever,
        context_builder=context_builder,
        llm=llm,
    )

    # --------------------------------------------------
    # 7. Ask a question
    # --------------------------------------------------

    answer = rag.ask(
        question="What is Python?",
        top_k=2,
    )

    print("\nRAG answer:")
    print(answer)

    # --------------------------------------------------
    # 8. Validate
    # --------------------------------------------------

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0