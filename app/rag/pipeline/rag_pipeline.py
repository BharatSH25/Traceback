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
        
        print(f"\n--- RAG RETRIEVAL FOR QUERY: '{query}' ---")
        if not chunks:
            print("No matching context found in Vector DB.")
        else:
            for i, chunk in enumerate(chunks):
                print(f"[{i+1}] Distance: {chunk['distance']:.4f} | Content: {chunk['text'][:100]}...")
        print("--- END RAG RETRIEVAL ---\n")
        
        return self.builder.build(chunks)
