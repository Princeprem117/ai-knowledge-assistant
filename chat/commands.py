from chat.chatbot import ChatBot
from knowledge.base_knowledge import BaseKnowledge

class CommandHandler:

    def __init__(
        self,chatbot: ChatBot,knowledge: BaseKnowledge,):
        self.chatbot = chatbot      # calling to llm
        self.knowledge = knowledge  # calling access to knowledge ingestion 

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

        if command.startswith("/add "):
            return self.add_document(command)

        if command.startswith("/ask"):
            return self.ask_knowledge(command)

        if command == "/list":
            return self.list_documents()
        if command.startswith("/remove "):
            return self.remove_document(command)

        return "Unknown command. Type /help for a list of available commands."

    # add document method
    def add_document(self, command):

        file_path = command[len("/add "):].strip()

        if not file_path:
                return (
                "Please provide a file path. "
                "Example: /add data/sample.txt"
                )

        try:
            chunks = self.knowledge.ingest_file(
                file_path
                )

            return (
                f"Document ingested successfully.\n"
                f"Chunks stored: {chunks}"
                )

        except ValueError as e:
            return str(e)

        except Exception as e:
            return f"Failed to ingest document: {e}"

    # Ask command
    def ask_knowledge(self, command):

        question = command[len("/ask "):].strip()

        if not question:
            return "Please provide a question. Example: /ask What is Python?"

        return self.chatbot.ask_knowledge(
        question=question,
        top_k=3,
        )

    def show_help(self):
        return """
        Available commands
        /help       - Show this Available commands
        /add <file_path>    - Add a document to the knowledge base
        /ask <question>     -Ask a question using the knowledge base
        /clear      - Clear the conversation history
        /new        - Start a new conversation history
        /history    - Show conversation history
        /list       - List documents in the knowledge base
        /remove <file_path> -   Remove a document from the knowledge base
        """

    # History command
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

    # Clear command
    def clear_history(self):
        self.chatbot.clear_history()
        return "Conversation history cleared."

    def new_chat(self):
        self.chatbot.new_chat()
        return "New conversation started."

    def list_documents(self):

        documents = self.knowledge.list_documents()

        if not documents:
            return "No documents found in the knowledge base."

        response = "Indexed documents:\n"

        sources = []

        for metadata in documents:
            source = metadata.get("source")

            if source and source not in sources:
                sources.append(source)

        for index, source in enumerate(sources, start=1):
            response += f"[{index}] {source}\n"

        return response.rstrip()

    # user command to remove docs
    def remove_document(self, command):

        file_path = command[len("/remove "):].strip()

        if not file_path:
            return (
            "Please provide a file path. "
            "Example: /remove data/sample.pdf"
            )

        try:
            chunks = self.knowledge.remove_document(
            file_path
            )

            if chunks == 0:
                return (
                "Document not found in the knowledge base."
                )

            return (
                f"Document removed successfully.\n"
                f"Chunks removed: {chunks}"
            )

        except Exception as e:
            return f"Failed to remove document: {e}"