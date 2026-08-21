from loaders.text_loader import TextLoader
from models.document import Document


def test_text_loader():

    loader = TextLoader()

    document = loader.load(
        "data/sample.txt"
    )

    print("\nLoaded document:")
    print(document)

    assert isinstance(document, Document)

    assert document.content.strip() != ""

    assert document.metadata["source"] == (
        "data/sample.txt"
    )

    assert document.metadata["type"] == "text"