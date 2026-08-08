from sentence_transformers import SentenceTransformer

from embeddings.base_embedding import BaseEmbedding
from config import EMBEDDING_MODEL_NAME


class SentenceTransformerEmbedding(BaseEmbedding):

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()