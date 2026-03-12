from app.rag.ingestion.embedding_generator import EmbeddingGenerator


class QueryEmbedder:
    def __init__(self) -> None:
        self._embedder = EmbeddingGenerator()

    def embed(self, query: str) -> list[float]:
        return self._embedder.embed(query)
