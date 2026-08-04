from chatbot import ChatBot
from storage import load_history , save_history

# Load the conversation history from the JSON file
history = load_history()
# Initialize the chatbot
chatbot = ChatBot(history)
# the chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "bye"]:
        break

    reply = chatbot.chat(user_input)
    print(f"\n AI: {reply}")
    print(f"{'_'*50}")
    
    save_history(chatbot.get_messages())