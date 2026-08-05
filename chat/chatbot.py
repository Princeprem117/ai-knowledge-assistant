from chat.prompts import SYSTEM_PROMPT

class ChatBot:
    def __init__(self,conversation_history, llm):
        self.llm = llm

# inditialize conversation_history with both history and initial system prompt
        self.conversation_history = conversation_history or [{"role": "system", "content": SYSTEM_PROMPT}]

# adding of user message to the conversation history
    def add_user_message(self, message: str)-> None:
        self.conversation_history.append({"role": "user", "content": message})

# adding of assistant message to the conversation history
    def add_assistant_message(self, message: str)-> None:
        self.conversation_history.append({"role": "assistant", "content": message})

# return the current conversation history
    def get_messages(self)-> list[dict]:
        return self.conversation_history
        

#saves generated response and adds assistant's reply to the conversation history
    def chat(self, user_message: str) -> str:
        self.add_user_message(user_message)
        reply = self.llm.generate(self.conversation_history)
        # saves history and adds the assistant's reply to the conversation history
        self.add_assistant_message(reply)
        return reply


# clears the conversation history and resets it to the initial system prompt
    def clear_history(self):
        self.conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def new_chat(self):
        self.clear_history()