from abc import ABC, abstractmethod
from models.document import Document


class BaseChunker(ABC):

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    def chunk(self, document: Document) -> list[Document]:
        pass