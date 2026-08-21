from knowledge.base_knowledge import BaseKnowledge


class FakeIngestionService:

    def ingest_file(self, file_path: str, user_id: str | None = None) -> int:
        return 5


class FakeRetriever:

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        user_id: str | None = None,
    ):
        return {
            "documents": [
                ["Python is a programming language."]
            ],
            "ids": [
                ["python_001"]
            ],
        }


def test_knowledge_base_ingest():

    knowledge_base = BaseKnowledge(
        ingestion_service=FakeIngestionService(),
        retriever=FakeRetriever(),
    )

    result = knowledge_base.ingest_file(
        "data/sample.txt"
    )

    assert result == 5


def test_knowledge_base_search():

    knowledge_base = BaseKnowledge(
        ingestion_service=FakeIngestionService(),
        retriever=FakeRetriever(),
    )

    results = knowledge_base.search(
        "What is Python?",
        top_k=2,
    )

    assert results["ids"][0][0] == "python_001"

    assert (
        results["documents"][0][0]
        == "Python is a programming language."
    )