from chat.chatbot import ChatBot
from storage import load_history, save_history
from chat.commands import CommandHandler
from llms.groq_client import GroqClient

from config import CHROMA_PERSIST_DIRECTORY

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding

from ingestion.pipeline import IngestionPipeline
from ingestion.service import DocumentIngestionService

from knowledge.base_knowledge import BaseKnowledge

from retrieval.retriever import Retriever
from retrieval.context_builder import ContextBuilder

from vectordb.chroma_db import ChromaVectorStore

from rag.pipeline import RAGPipeline

# Load the conversation history from the JSON file
history = load_history()

# Initialize the Groq client
llm = GroqClient()

# Embedding model
embedder = SentenceTransformerEmbedding()

# Vector database
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

# context builder
context_builder = ContextBuilder()

# RAG pipeline
rag_pipeline = RAGPipeline(
    retriever=retriever,
    context_builder=context_builder,
    llm=llm,
)

# Knowledge base
knowledge = BaseKnowledge(
    ingestion_service=ingestion_service,
    retriever=retriever,
)

print("Knowledge Base initialized successfully.")


# Initialize the chatbot
chatbot = ChatBot(
    conversation_history=history,
    llm=llm,
    rag_pipeline=rag_pipeline,
)
# Initialize the command handler
command_handler = CommandHandler(
    chatbot=chatbot,
    knowledge=knowledge,
)
# the chat loop
while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "bye"]:
        break

    if command_handler.is_command(user_input):
        response = command_handler.handle_command(user_input)

        print(f"\nAI: {response}")
        print("_" * 50)

        save_history(chatbot.get_messages())
        continue

    reply = chatbot.chat(user_input)

    print(f"\nAI: {reply}")
    print("_" * 50)

    save_history(chatbot.get_messages())

