from chat.chatbot import ChatBot
class CommandHandler:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def is_command(self, command):
        return command.startswith("/")
    
    def handle_command(self, command):
        if command == "/help":
            return self.show_help()
        if command == "/clear":
            return self.clear_history()
        if command == "/new":
            return self.new_chat()
        if command == "/history":
            return self.show_history()
        return "Unknown command. Type /help for a list of available commands."

    def show_help(self):
        return """
        Available commands
        /help   - Show this Available commands
        /clear  - Clear the conversation history
        /new    - Start a new conversation history
        /history- Show conversation history
        """

    def show_history(self):
        messages = self.chatbot.get_messages()
        history=[]
        if not messages:
            return "No conversation history available."
        for msg in messages:
            if msg["role"] == "system":
                continue  # Skip the system prompt
            # use you for user messages and AI for assistant messages
            if msg["role"] == "user":
                history.append(f"You: {msg['content']}")
            if msg["role"] == "assistant":
                history.append(f"AI: {msg['content']}")

        return "\n".join(history)

    
    def clear_history(self):
        self.chatbot.clear_history()
        return "Conversation history cleared."

    def new_chat(self):
        self.chatbot.new_chat()
        return "New conversation started."
