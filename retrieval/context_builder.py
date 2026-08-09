class ContextBuilder:
    """
    Builds an LLM-ready context from retrieved documents.
    """

    def build(self, retrieved_documents: list[str]) -> str:
        """
        Combine retrieved documents into a single context string.
        """

        return "\n\n".join(retrieved_documents)
