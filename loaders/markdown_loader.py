from loaders.base_loader import BaseLoader
from models.document import Document


class MarkdownLoader(BaseLoader):

    def load(self, file_path: str) -> Document:
        """
        Load Markdown data from a file.
        """

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        return Document(
            content=text,
            metadata={
                "source": file_path,
                "type": "markdown",
            },
        )