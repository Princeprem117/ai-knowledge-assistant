import re

from chunkers.base_chunker import BaseChunker
from embeddings.base_embedding import BaseEmbedding
from models.document import Document
from vectordb.base_db import BaseVectorStore


class IngestionPipeline:

    def __init__(
        self,
        chunker: BaseChunker,
        embedding_model: BaseEmbedding,
        vector_store: BaseVectorStore,
    ):
        self.chunker = chunker
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def ingest(self, documents: list[Document]) -> int:
        """
        Chunk documents, generate embeddings,
        and store the chunks in the vector database.

        Returns the number of chunks stored.
        """

        all_chunks = []

        # 1. Chunk all documents
        for document in documents:
            chunks = self.chunker.chunk(document)
            all_chunks.extend(chunks)

        if not all_chunks:
            return 0

        # 2. Generate embeddings
        embeddings = [
            self.embedding_model.embed(chunk.content)
            for chunk in all_chunks
        ]

        # 3. Prepare data for vector store

        contents = [
                chunk.content
                for chunk in all_chunks
            ]

        metadatas = []
        source_paths = []

        for chunk in all_chunks:

            metadata = dict(chunk.metadata)

            source = metadata.get("source")

            # Keep the original source for deterministic IDs.
            source_paths.append(source)

                # Keep the original source path in metadata.
            if source:
                metadata["source"] = str(source)

                metadatas.append(metadata)

        # 4. Generate stable IDs

        ids = []
        source_counters = {}

        for source in source_paths:
            source_id = re.sub(
                r"[^a-zA-Z0-9]+",
                "_",
                str(source)
            ).strip("_").lower()

            counter = source_counters.get(
                source_id,
                0
            )

            chunk_id = (
                f"{source_id}_chunk_{counter:03d}"
            )

            ids.append(chunk_id)

            source_counters[source_id] = counter + 1

        # 5. Store chunks in vector database
        self.vector_store.add(
            documents=contents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

        return len(all_chunks)