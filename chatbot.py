from groq import Groq
from prompts import SYSTEM_PROMPT
from config import GROQ_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE

class ChatBot:
    def __init__(self,conversation_history):
        self.model = MODEL_NAME
        self.client = Groq(api_key=GROQ_API_KEY)
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        if conversation_history:
            self.messages = conversation_history
        else:
             # Initialize with the system prompt
            self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
# adding of user message to the conversation history
    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})
# adding of assistant message to the conversation history
    def add_assistant_message(self, message):
        self.messages.append({"role": "assistant", "content": message})
# return the current conversation history
    def get_messages(self):
        return self.messages

# generating the response from the  model by calling Groq API
    def generate_response(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return response.choices[0].message.content

#saves generated response and adds assistant's reply to the conversation history
    def chat(self, user_message):
        self.add_user_message(user_message)
        reply = self.generate_response()
        # saves history and adds the assistant's reply to the conversation history
        self.add_assistant_message(reply)
        return reply