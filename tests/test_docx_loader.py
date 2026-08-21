from loaders.docx_loader import DocxLoader


def test_docx_loader():

    loader = DocxLoader()

    document = loader.load(
        "data/sample.docx"
    )

    print("\nLoaded DOCX:")
    print(document)

    assert document.content
    assert "Python" in document.content

    assert document.metadata["source"] == (
        "data/sample.docx"
    )

    assert document.metadata["type"] == "docx"