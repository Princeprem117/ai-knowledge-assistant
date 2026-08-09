from llms.base_llm import BaseLLM
from retrieval.context_builder import ContextBuilder
from retrieval.retriever import Retriever


class RAGPipeline:
    """
    Coordinates retrieval, context construction,
    and LLM generation.
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
        """
        Answer a question using retrieved knowledge.
        """

        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        documents = results["documents"][0]

        context = self.context_builder.build(
            documents
        )

        prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:
""".strip()

        return self.llm.generate(prompt)