from app.dependencies import create_knowledge_base

from chat.chatbot import ChatBot
from chat.commands import CommandHandler
from storage import load_history, save_history

from retrieval.context_builder import ContextBuilder
from rag.pipeline import RAGPipeline


# Load conversation history
history = load_history()


# Initialize shared application dependencies
knowledge, retriever, llm = create_knowledge_base()

print("Knowledge Base initialized successfully.")


# Context builder
context_builder = ContextBuilder()


# RAG pipeline
rag_pipeline = RAGPipeline(
    retriever=retriever,
    context_builder=context_builder,
    llm=llm,
)


# Chatbot
chatbot = ChatBot(
    conversation_history=history,
    llm=llm,
    rag_pipeline=rag_pipeline,
)


# Command handler
command_handler = CommandHandler(
    chatbot=chatbot,
    knowledge=knowledge,
)


# Chat loop
while True:

    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "bye"]:
        break

    if command_handler.is_command(user_input):

        response = command_handler.handle_command(
            user_input
        )

        print(f"\nAI: {response}")
        print("_" * 50)

        save_history(
            chatbot.get_messages()
        )

        continue

    reply = chatbot.chat(user_input)

    print(f"\nAI: {reply}")
    print("_" * 50)

    save_history(
        chatbot.get_messages()
    )