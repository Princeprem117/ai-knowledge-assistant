from embeddings.base_embedding import BaseEmbedding
from vectordb.base_db import BaseVectorStore


class Retriever:
    """
    Retrieves relevant documents from the vector store
    using semantic similarity.
    """

    def __init__(
        self,
        embedding_model: BaseEmbedding,
        vector_store: BaseVectorStore,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict:
        """
        Convert the query into an embedding and
        retrieve the most relevant documents.
        """

        query_embedding = self.embedding_model.embed(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        # Temporary diagnostic output
        print("\n--- Retrieval Debug ---")
        print(f"Query: {query}")

        distances = results.get("distances", [[]])[0]
        documents = results.get("documents", [[]])[0]

        for index, (distance, document) in enumerate(
            zip(distances, documents),
            start=1,
        ):
            preview = document[:100].replace("\n", " ")

            print(
                f"{index}. distance={distance:.4f} "
                f"| document={preview}"
            )

        print("-----------------------\n")

        return results