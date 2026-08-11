from config import CHROMA_PERSIST_DIRECTORY

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding

from ingestion.pipeline import IngestionPipeline
from ingestion.service import DocumentIngestionService

from knowledge.base_knowledge import BaseKnowledge

from llms.groq_client import GroqClient

from retrieval.retriever import Retriever
from retrieval.context_builder import ContextBuilder

from rag.pipeline import RAGPipeline

from vectordb.chroma_db import ChromaVectorStore


def create_knowledge_base():
    """
    Create and configure the knowledge base and
    all of its required dependencies.
    """

    # LLM
    llm = GroqClient()

    # Embedding model
    embedder = SentenceTransformerEmbedding()

    # Vector store
    vector_store = ChromaVectorStore(
        persist_directory=CHROMA_PERSIST_DIRECTORY
    )

    # Chunker
    chunker = RecursiveChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    # Ingestion pipeline
    ingestion_pipeline = IngestionPipeline(
        chunker=chunker,
        embedding_model=embedder,
        vector_store=vector_store,
    )

    # Document ingestion service
    ingestion_service = DocumentIngestionService(
        ingestion_pipeline=ingestion_pipeline,
    )

    # Retriever
    retriever = Retriever(
        embedding_model=embedder,
        vector_store=vector_store,
    )

    # Context builder
    context_builder = ContextBuilder()
    
    # RAG pipeline
    rag_pipeline = RAGPipeline(
        retriever=retriever,
        context_builder= context_builder,
        llm=llm,
)

    # Knowledge base
    knowledge = BaseKnowledge(
        ingestion_service=ingestion_service,
        retriever=retriever,
    )

    return knowledge, rag_pipeline, llm