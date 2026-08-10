from llms.base_llm import BaseLLM
from retrieval.context_builder import ContextBuilder
from retrieval.retriever import Retriever


class RAGPipeline:
    """
    Coordinates retrieval, context construction,
    and language model generation.
    """

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        llm: BaseLLM,
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.llm = llm

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:

        # Retrieve relevant documents
        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        documents = results["documents"][0]

        # Build context from retrieved documents
        context = self.context_builder.build(
            documents
        )

        # Create messages for the LLM
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI Knowledge Assistant. "
                    "Answer the user's question using the provided context. "
                    "If the answer cannot be found in the context, "
                    "say that you don't have enough information."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n"
                    f"{context}\n\n"
                    f"Question:\n"
                    f"{question}"
                ),
            },
        ]

        # Generate answer
        return self.llm.generate(messages)