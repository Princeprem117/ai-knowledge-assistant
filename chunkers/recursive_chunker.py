from chunkers.base_chunker import BaseChunker
from models.document import Document

class RecursiveChunker(BaseChunker):

    # the method which orchestrats the document from splitting into chunks to it's chunks  documents creation
    def chunk(self, document: Document) -> list[Document]:
        # Implement the recursive chunking logic here
        text = document.content
        chunks = self._split_text(text)
        documents = self._create_documents(chunks, document.metadata)
        return documents

    # method for spliting the document into req. small pieces (chunks)
    def _split_text(self, text: str) -> list[str]:
        # Implement the logic to split the text into chunks based on chunk_size and chunk_overlap
        start = 0
        chunks = []

        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])

            if end >= len(text):
                break
            next_start = end - self.chunk_overlap

            if next_start <= start:
                next_start = end
            start = next_start
        return chunks

    # method for creating documents of chunks 
    def _create_documents(self, chunks: list[str], metadata: dict)-> list[Document]:
        # Implement the logic to create Document objects from the text chunks
        documents = []
        for chunk in chunks:
            documents.append(Document(
                content=chunk,
                metadata=metadata.copy()))
        return documents