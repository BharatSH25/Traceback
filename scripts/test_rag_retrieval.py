import asyncio
from app.rag.retrieval.vector_search import VectorSearch
from app.rag.constants import EMBEDDING_DIM

async def test_retrieval():
    searcher = VectorSearch()
    
    # We'll search using a vector that matches INC-003 (index 20)
    # ingest_dummy_data.py used index i*10, so INC-003 was at index 20
    query_vector = [0.0] * EMBEDDING_DIM
    query_vector[20] = 1.0  # Matches index of INC-003
    
    print(f"Searching for most similar incident (Query Vector index 20 = 1.0)...")
    results = await searcher.search(query_vector, k=2)
    
    if not results:
        print("No results found!")
        return

    for i, res in enumerate(results):
        print(f"\nResult {i+1} (Distance: {res['distance']:.4f}):")
        print(f"Content: {res['text']}")
        print(f"Metadata: {res['metadata']}")

if __name__ == "__main__":
    asyncio.run(test_retrieval())
