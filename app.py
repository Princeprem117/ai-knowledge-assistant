from chat.chatbot import ChatBot
from storage import load_history, save_history
from chat.commands import CommandHandler
from llms.groq_client import GroqClient

# Load the conversation history from the JSON file
history = load_history()

# Initialize the Groq client
llm = GroqClient()

# Initialize the chatbot
chatbot = ChatBot(history,llm)
# Initialize the command handler
command_handler = CommandHandler(chatbot)

# the chat loop
while True:
    user_input = input("You: ")

# Check if the user wants to exit the application
    if user_input.lower() in ["exit", "bye"]:
        break

# Check if the user input is a command
    if command_handler.is_command(user_input):
            response = command_handler.handle_command(user_input)
            print(f"\n {response}")
            print(f"{'_'*50}")
            continue

    reply = chatbot.chat(user_input)
    print(f"\n AI: {reply}")
    print(f"{'_'*50}")
    
    save_history(chatbot.get_messages())