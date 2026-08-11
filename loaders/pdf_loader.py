from pypdf import PdfReader

from loaders.base_loader import BaseLoader
from models.document import Document


class PdfLoader(BaseLoader):

    def load(self, file_path: str) -> Document:
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        content = "\n\n".join(pages)

        return Document(
            content=content,
            metadata={
                "source": file_path,
                "type": "pdf",
            },
        )