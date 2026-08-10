from chat.prompts import SYSTEM_PROMPT
from rag.pipeline import RAGPipeline


class ChatBot:

    def __init__(
        self,
        conversation_history,
        llm,
        rag_pipeline: RAGPipeline | None = None,
        max_history_messages=10,
    ):
        self.llm = llm
        self.rag_pipeline = rag_pipeline
        self.max_history_messages = max_history_messages

        # Initialize conversation history
        self.conversation_history = (
            conversation_history
            or [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                }
            ]
        )

    def add_user_message(self, message: str) -> None:
        self.conversation_history.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str) -> None:
        self.conversation_history.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def get_messages(self) -> list[dict]:
        return self.conversation_history

    def chat(self, user_message: str) -> str:

        self.add_user_message(user_message)

        reply = self.llm.generate(
            self.get_llm_messages()
        )

        self.add_assistant_message(reply)

        return reply


    def ask_knowledge(
        self,
        question: str,
        top_k: int = 3,
    ) -> str:

        if self.rag_pipeline is None:
            return "Knowledge base is not available."

        answer = self.rag_pipeline.ask(
            question=question,
            top_k=top_k,
        )

        return answer

    def clear_history(self):
        self.conversation_history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]
    # method for new chat
    def new_chat(self):
        self.clear_history()

    # method for LLM context
    def get_llm_messages(self) -> list[dict]:
        """
        Return the messages that should be sent to the LLM.
        Keeps the system prompt and the most recent conversation messages.
        """

        system_message = self.conversation_history[0]

        recent_messages = self.conversation_history[1:][
            -self.max_history_messages:
            ]

        return [system_message] + recent_messages