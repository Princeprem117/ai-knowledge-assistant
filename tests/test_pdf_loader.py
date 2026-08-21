from loaders.pdf_loader import PdfLoader
from models.document import Document


def test_pdf_loader():

    loader = PdfLoader()

    document = loader.load(
        "data/sample.pdf"
    )

    print("\nLoaded PDF:")
    print(document)

    assert isinstance(document, Document)

    assert document.content.strip() != ""

    assert document.metadata["source"] == "data/sample.pdf"

    assert document.metadata["type"] == "pdf"