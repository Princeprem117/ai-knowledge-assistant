from config import GROQ_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE
from groq import Groq
from llms.base_llm import BaseLLM

class GroqClient(BaseLLM):
    def __init__(self)-> None:
        self.model = MODEL_NAME
        self.client = Groq(api_key=GROQ_API_KEY)
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE

    def generate(self, messages: list[dict]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I encountered an error while processing your request."