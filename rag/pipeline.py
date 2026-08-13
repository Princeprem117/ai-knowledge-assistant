from pathlib import Path

from llms.base_llm import BaseLLM
from retrieval.context_builder import ContextBuilder
from retrieval.retriever import Retriever


class RAGPipeline:
    """
    Coordinates retrieval, context construction,
    language model generation, and source citations.

    Supports hybrid behavior:
    - Uses retrieved documents when relevant.
    - Falls back to general LLM knowledge when
      retrieved documents are not relevant.
    """

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        llm: BaseLLM,
        relevance_threshold: float = 1.5
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.llm = llm
        self.relevance_threshold = relevance_threshold
    def ask(
        self,
        question: str,
        top_k: int = 3,
    ) -> str:

        # --------------------------------------------------
        # 1. Retrieve relevant documents
        # --------------------------------------------------

        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        #--------------------------------------------------
        # 2. Determine whether retrieved documents
        #    are actually relevant
        # --------------------------------------------------

        # ChromaDB distance:
        # smaller distance = more similar
        #
        # This is an initial threshold and can be tuned
        # later after evaluating more documents/questions.

        relevant_documents = []
        relevant_metadatas = []
        relevant_distances = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):

            if distance <= self.relevance_threshold:

                relevant_documents.append(document)

                relevant_metadatas.append(metadata)

                relevant_distances.append(distance)

        # --------------------------------------------------
        # 3. Document-related question
        # --------------------------------------------------

        if relevant_documents:

            context = self.context_builder.build(
                relevant_documents
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI Knowledge Assistant. "

                        "Use the provided document context "
                        "whenever it contains information "
                        "relevant to the user's question. "

                        "If the context does not contain enough "
                        "information to answer the question, "
                        "you may use your general knowledge. "

                        "Clearly distinguish information from "
                        "the documents from information based "
                        "on general knowledge. "

                        "Do not invent information and do not "
                        "claim that something comes from the "
                        "documents unless it is supported by "
                        "the provided context."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Document Context:\n"
                        f"{context}\n\n"
                        f"Question:\n"
                        f"{question}"
                    ),
                },
            ]

            answer = self.llm.generate(messages)

            # --------------------------------------------------
            # 4. Build source citations
            # --------------------------------------------------

            source_scores = {}

            for metadata, distance in zip(
                relevant_metadatas,
                relevant_distances,
            ):

                source = metadata.get("source")

                if not source:
                    continue

                filename = Path(source).name

                if (
                    filename not in source_scores
                    or distance < source_scores[filename]
                ):
                    source_scores[filename] = distance

            sorted_sources = sorted(
                source_scores.items(),
                key=lambda item: item[1],
            )

            if sorted_sources:

                answer += "\n\nSources:\n"

                for index, (source, distance) in enumerate(
                    sorted_sources,
                    start=1,
                ):
                    answer += f"\n[{index}] {source}\n"

            return answer

        # --------------------------------------------------
        # 5. General knowledge fallback
        # --------------------------------------------------

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI Knowledge Assistant. "

                    "No relevant document context was found "
                    "for this question. "

                    "Answer the user's question and "
                    "Do not claim that the answer comes from "
                    "the user's documents."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        return self.llm.generate(messages)