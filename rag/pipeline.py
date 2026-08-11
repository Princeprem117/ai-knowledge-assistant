from llms.base_llm import BaseLLM
from retrieval.context_builder import ContextBuilder
from retrieval.retriever import Retriever


class RAGPipeline:
    """
    Coordinates retrieval, context construction,
    language model generation, and source citations.
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

        # 1. Retrieve relevant documents
        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        # 2. Build context from retrieved documents
        context = self.context_builder.build(
            documents
        )

        # 3. Create messages for the LLM
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI Knowledge Assistant. "
                    "Answer the user's question using only the "
                    "provided context. "
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

        # 4. Generate answer
        answer = self.llm.generate(messages)

        # 5. Build source citations from metadata
        sources = []

        for metadata in metadatas:
            source = metadata.get("source")

            if source and source not in sources:
                sources.append(source)

        # 6. Add citations to the answer
        if sources:
            answer += "\n\nSources:\n"

            for index, source in enumerate(sources, start=1):

                answer += f"[{index}] {source}\n"


        return answer