from retrieval.context_builder import ContextBuilder


def test_context_builder():
    builder = ContextBuilder()

    documents = [
        "Python is a programming language.",
        "Python supports object-oriented programming.",
    ]

    context = builder.build(documents)

    print("Generated context:")
    print(context)

    assert "Python is a programming language." in context
    assert "Python supports object-oriented programming." in context

if __name__ == "__main__":
    test_context_builder()