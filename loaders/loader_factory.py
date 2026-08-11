from pathlib import Path

from loaders.docx_loader import DocxLoader
from loaders.base_loader import BaseLoader
from loaders.text_loader import TextLoader
from loaders.pdf_loader import PdfLoader
from loaders.markdown_loader import MarkdownLoader


class LoaderFactory:

    @staticmethod
    def get_loader(file_path: str) -> BaseLoader:
        """
        Return the appropriate loader based on file extension.
        """

        extension = Path(file_path).suffix.lower()

        if extension == ".txt":
            return TextLoader()

        if extension == ".pdf":
            return PdfLoader()

        if extension in {".md", ".markdown"}:
            return MarkdownLoader()

        if extension == ".docx":
            return DocxLoader()

        raise ValueError(
            f"Unsupported file type: {extension}"
        )