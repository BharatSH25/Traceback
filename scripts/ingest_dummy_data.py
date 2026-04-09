import asyncio
import random
from app.rag.ingestion.vector_indexer import VectorIndexer
from app.rag.constants import EMBEDDING_DIM

async def ingest_samples():
    indexer = VectorIndexer()
    
    samples = [
        {
            "doc_id": "INC-001",
            "content": "Payment service timeout occurred due to high database locks on the orders table. System load was 95%.",
            "metadata": {"service": "payment", "severity": "high"}
        },
        {
            "doc_id": "INC-002",
            "content": "Frontend latency increased after deployment v1.2.3. Root cause: inefficient CSS rendering in the dashboard.",
            "metadata": {"service": "frontend", "severity": "medium"}
        },
        {
            "doc_id": "INC-003",
            "content": "Memory leak detected in the notification worker. Garbage collection was unable to reclaim memory from the socket connections.",
            "metadata": {"service": "notifications", "severity": "high"}
        },
        {
            "doc_id": "INC-004",
            "content": "DNS resolution failure for internal microservices. CoreDNS pod was in CrashLoopBackOff state.",
            "metadata": {"service": "infrastructure", "severity": "critical"}
        }
    ]

    print(f"Starting ingestion of {len(samples)} dummy records...")
    
    for i, sample in enumerate(samples):
        # Create a "pseudo-semantic" vector:
        # We'll put a 1.0 at index i*10 to make them somewhat distinct
        embedding = [0.0] * EMBEDDING_DIM
        embedding[i * 10] = 1.0
        
        await indexer.upsert(
            doc_id=sample["doc_id"],
            chunk_index=0,
            content=sample["content"],
            embedding=embedding,
            metadata=sample["metadata"]
        )
        print(f"Ingested {sample['doc_id']}")

    print("Ingestion complete!")

if __name__ == "__main__":
    asyncio.run(ingest_samples())
