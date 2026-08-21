import pytest

from loaders.docx_loader import DocxLoader
from loaders.loader_factory import LoaderFactory
from loaders.text_loader import TextLoader
from loaders.pdf_loader import PdfLoader
from loaders.markdown_loader import MarkdownLoader

# text loader
def test_text_loader_selection():

    loader = LoaderFactory.get_loader(
        "data/sample.txt"
    )

    assert isinstance(loader, TextLoader)

#pdf loader
def test_pdf_loader_selection():

    loader = LoaderFactory.get_loader(
        "data/sample.pdf"
    )

    assert isinstance(loader, PdfLoader)

# markdown file  loader
def test_markdown_loader_selection():

    loader = LoaderFactory.get_loader(
        "data/sample.md"
    )

    assert isinstance(loader, MarkdownLoader)
# docx file loader
def test_docx_loader_selection():

    loader = LoaderFactory.get_loader(
        "data/sample.docx"
    )

    assert isinstance(
        loader,
        DocxLoader
    )
# ValueError method
def test_unsupported_file_type():

    with pytest.raises(ValueError):

        LoaderFactory.get_loader(
            "data/sample.xyz"
        )