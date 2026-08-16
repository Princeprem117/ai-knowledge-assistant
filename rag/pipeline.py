from pathlib import Path

from config import RAG_RELEVANCE_THRESHOLD

from llms.base_llm import BaseLLM
from retrieval.context_builder import ContextBuilder
from retrieval.retriever import Retriever


class RAGPipeline:
    """
    Strict Retrieval-Augmented Generation pipeline.

    The LLM is allowed to answer only from
    retrieved document context.
    """

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        llm: BaseLLM,
        relevance_threshold: float = RAG_RELEVANCE_THRESHOLD,
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
        # 1. Retrieve documents
        # --------------------------------------------------

        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        # --------------------------------------------------
        # 2. Relevance filtering
        # --------------------------------------------------

        print("\n--- Relevance Evaluation ---")
        print(f"Threshold: {self.relevance_threshold}")

        relevant_documents = []
        relevant_metadatas = []
        relevant_distances = []

        for index, (
            document,
            metadata,
            distance,
        ) in enumerate(
            zip(
                documents,
                metadatas,
                distances,
            ),
            start=1,
        ):

            if distance <= self.relevance_threshold:

                print(
                    f"{index}. distance={distance:.4f} → RELEVANT"
                )

                relevant_documents.append(document)
                relevant_metadatas.append(metadata)
                relevant_distances.append(distance)

            else:

                print(
                    f"{index}. distance={distance:.4f} → NOT RELEVANT"
                )

        print(
            f"Relevant results: "
            f"{len(relevant_documents)}/{len(documents)}"
        )

        # --------------------------------------------------
        # 3. No relevant context
        # --------------------------------------------------

        if not relevant_documents:

            print(
                "Decision: NO RELEVANT DOCUMENT CONTEXT"
            )
            print("-------------------------------\n")

            return (
                "I couldn't find information about this "
                "in the provided documents."
            )

        # --------------------------------------------------
        # 4. Build context
        # --------------------------------------------------

        print(
            "Decision: DOCUMENT CONTEXT USED"
        )
        print("-------------------------------\n")

        context = self.context_builder.build(
            relevant_documents
        )

        # --------------------------------------------------
        # 5. Strict RAG prompt
        # --------------------------------------------------

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI Knowledge Assistant "
                    "that answers questions using only "
                    "the provided document context.\n\n"

                    "STRICT RULES:\n"
                    "1. Use only information contained "
                    "in the provided context.\n"
                    "2. Do not use your general knowledge.\n"
                    "3. Do not guess or invent information.\n"
                    "4. If the context does not contain "
                    "enough information to answer the "
                    "question, say that the information "
                    "is not available in the provided "
                    "documents.\n"
                    "5. Do not claim information comes "
                    "from the documents unless it is "
                    "supported by the context."
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

        # --------------------------------------------------
        # 6. Generate answer
        # --------------------------------------------------

        answer = self.llm.generate(
            messages
        )

        # --------------------------------------------------
        # 7. Build source citations
        # --------------------------------------------------

        source_scores = {}

        for metadata, distance in zip(
            relevant_metadatas,
            relevant_distances,
        ):

            filename = metadata.get("filename")

            if not filename:
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

            for index, (
                source,
                distance,
            ) in enumerate(
                sorted_sources,
                start=1,
            ):

                answer += (
                    f"\n[{index}] {source}\n"
                )

        return answer