from chunkers.base_chunker import BaseChunker
from models.document import Document


class RecursiveChunker(BaseChunker):

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 60,
    ):
        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.separators = [
            "\n\n",     # paragraph
            "\n",       # line
            ". ",       # sentence
            " ",        # word
            "",         # character
        ]

    def chunk(self, document: Document) -> list[Document]:

        text = document.content.strip()

        chunks = self._split_text(
            text,
            self.separators,
        )

        chunks = self._add_overlap(chunks)

        return self._create_documents(
            chunks,
            document.metadata,
        )

    def _split_text(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:

        # If text already fits inside the target size,
        # no further splitting is necessary.

        if len(text) <= self.chunk_size:
            return [text]

        # If there are no more separators,
        # fall back to character-level splitting.

        if not separators:
            return self._split_by_characters(text)

        separator = separators[0]

        # Empty separator means character-level splitting.
        if separator == "":
            return self._split_by_characters(text)

        parts = text.split(separator)

        chunks = []
        current = ""

        for part in parts:

            if not part:
                continue

            if not current:
                current = part
                continue

            candidate = current + separator + part

            if len(candidate) <= self.chunk_size:
                current = candidate

            else:
                # Current piece is ready.
                chunks.extend(
                    self._split_text(
                        current,
                        separators[1:],
                    )
                )

                current = part

        if current:
            chunks.extend(
                self._split_text(
                    current,
                    separators[1:],
                )
            )

        return chunks

    def _split_by_characters(
        self,
        text: str,
    ) -> list[str]:

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunks.append(
                text[start:end]
            )

            start = end

        return chunks

    def _get_overlap(
        self,
        previous_chunk: str,
        next_chunk: str,
    ) -> str:

        # Space available inside the next chunk
        available_space = (
            self.chunk_size - len(next_chunk)
        )

        if available_space <= 1:
            return ""

        target_overlap = min(
            self.chunk_overlap,
            available_space - 1,
        )

        words = previous_chunk.split()

        overlap_words = []
        current_length = 0

        # Start from the end of the previous chunk
        for word in reversed(words):

            added_length = len(word)

            if overlap_words:
                added_length += 1  # space between words

            if current_length + added_length > target_overlap:
                break

            overlap_words.insert(0, word)
            current_length += added_length

        return " ".join(overlap_words)


    def _add_overlap(
        self,
        chunks: list[str],
    ) -> list[str]:

        if self.chunk_overlap == 0:
            return chunks

        result = [chunks[0]]

        for index in range(1, len(chunks)):

            previous_chunk = chunks[index - 1]
            current_chunk = chunks[index]

            overlap = self._get_overlap(
                previous_chunk,
                current_chunk,
            )

            if overlap:
                current_chunk = (
                    overlap + " " + current_chunk
                )

            result.append(current_chunk)

        return result

    def _create_documents(
        self,
        chunks: list[str],
        metadata: dict,
    ) -> list[Document]:

        documents = []

        for chunk in chunks:

            documents.append(
                Document(
                    content=chunk.strip(),
                    metadata=metadata.copy(),
                )
            )

        return documents