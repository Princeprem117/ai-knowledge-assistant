from config import (
    CHROMA_PERSIST_DIRECTORY,
    RAG_RELEVANCE_THRESHOLD,
 )

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding

from ingestion.pipeline import IngestionPipeline
from ingestion.service import DocumentIngestionService

from llms.groq_client import GroqClient

from retrieval.retriever import Retriever
from retrieval.context_builder import ContextBuilder

from rag.pipeline import RAGPipeline
from rag.service import RAGService

from services.document_service import DocumentService

from vectordb.chroma_db import ChromaVectorStore


def create_knowledge_base()-> RAGService:
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

    # Document service
    document_service = DocumentService(
        vector_store=vector_store,
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
        relevance_threshold=RAG_RELEVANCE_THRESHOLD,
)


    # Application-level RAG service
    rag_service = RAGService(
        rag_pipeline=rag_pipeline,
        ingestion_service=ingestion_service,
    )

    return rag_service, document_service