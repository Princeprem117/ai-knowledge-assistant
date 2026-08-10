from loaders.loader_factory import LoaderFactory
from ingestion.pipeline import IngestionPipeline


class DocumentIngestionService:

    def __init__(
        self,
        ingestion_pipeline: IngestionPipeline,
    ):
        self.ingestion_pipeline = ingestion_pipeline

    def ingest_file(self, file_path: str) -> int:
        """
        Load a file and ingest it into the vector store.

        Returns the number of chunks stored.
        """

        # 1. Select appropriate loader
        loader = LoaderFactory.get_loader(
            file_path
        )

        # 2. Load file into Document
        document = loader.load(
            file_path
        )

        # 3. Send Document to ingestion pipeline
        return self.ingestion_pipeline.ingest(
            [document]
        )