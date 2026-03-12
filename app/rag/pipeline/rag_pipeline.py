from app.rag.retrieval.query_embedder import QueryEmbedder
from app.rag.retrieval.vector_search import VectorSearch
from app.rag.retrieval.context_builder import ContextBuilder


class RagPipeline:
    def __init__(self) -> None:
        self.embedder = QueryEmbedder()
        self.search = VectorSearch()
        self.builder = ContextBuilder()

    async def run(self, query: str) -> str:
        embedding = self.embedder.embed(query)
        chunks = await self.search.search(embedding)
        return self.builder.build(chunks)
