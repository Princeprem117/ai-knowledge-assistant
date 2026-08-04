from groq import Groq
from chat.prompts import SYSTEM_PROMPT
from config import GROQ_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE

class ChatBot:
    def __init__(self,conversation_history):
        self.model = MODEL_NAME
        self.client = Groq(api_key=GROQ_API_KEY)
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE

# inditialize conversation_history with both history and initial system prompt
        self.conversation_history = conversation_history or [{"role": "system", "content": SYSTEM_PROMPT}]

# adding of user message to the conversation history
    def add_user_message(self, message):
        self.conversation_history.append({"role": "user", "content": message})

# adding of assistant message to the conversation history
    def add_assistant_message(self, message):
        self.conversation_history.append({"role": "assistant", "content": message})

# return the current conversation history
    def get_messages(self):
        return self.conversation_history

# generating the response from the  model by calling Groq API
    def generate_response(self):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I encountered an error while processing your request."

#saves generated response and adds assistant's reply to the conversation history
    def chat(self, user_message):
        self.add_user_message(user_message)
        reply = self.generate_response()
        # saves history and adds the assistant's reply to the conversation history
        self.add_assistant_message(reply)
        return reply