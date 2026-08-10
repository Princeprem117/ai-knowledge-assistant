from PyPDF2 import PdfReader

from loaders.base_loader import BaseLoader
from models.document import Document


class PdfLoader(BaseLoader):

    def load(self, file_path: str) -> Document:
        """
        Load text from a PDF file.
        """

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return Document(
            content=text,
            metadata={
                "source": file_path,
                "type": "pdf",
            },
        )