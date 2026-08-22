from app.dependencies import create_knowledge_base

from chat.chatbot import ChatBot
from chat.commands import CommandHandler
from storage import load_history, save_history




# Load conversation history
history = load_history()


# Initialize shared application dependencies
rag_service, document_service = create_knowledge_base()

print("Knowledge Base initialized successfully.")


# Chatbot
chatbot = ChatBot(
    conversation_history=history,
    llm=rag_service.rag_pipeline.llm,
    rag_pipeline=rag_service.rag_pipeline,
)


# Command handler
command_handler = CommandHandler(
    chatbot=chatbot,
    knowledge=document_service,
)


# Main Chat loop
while True:

    user_input = input("You: ").strip()
    # Exit application
    if user_input.lower() in ["exit", "bye"]:
        break
        # Hnadling commands
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
        # Normal chat
    reply = chatbot.chat(user_input)

    print(f"\nAI: {reply}")
    print("_" * 50)

    save_history(
        chatbot.get_messages()
    )