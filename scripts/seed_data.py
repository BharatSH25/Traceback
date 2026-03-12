"""Seed mock RAG documents into Postgres/pgvector."""

import asyncio

from app.rag.ingestion.chunker import Chunker
from app.rag.ingestion.embedding_generator import EmbeddingGenerator
from app.rag.ingestion.vector_indexer import VectorIndexer


DOCS = [
    {
        "doc_id": "runbook-incident-upload-service",
        "title": "Upload Service Incident Runbook",
        "text": (
            "If upload requests fail with 5xx, check recent deployments and timeout configs. "
            "Look for spikes in request latency and upstream storage errors. "
            "Rollback the last deployment if error rate increased after deploy."
        ),
        "metadata": {"service": "incident-upload-service", "type": "runbook"},
    },
    {
        "doc_id": "postmortem-queue-backlog",
        "title": "Queue Backlog Postmortem",
        "text": (
            "Queue backlog incidents often follow a sudden drop in workers or a misconfigured concurrency limit. "
            "Verify worker health and concurrency settings, then scale workers if needed."
        ),
        "metadata": {"service": "incident-upload-service", "type": "postmortem"},
    },
]


async def main() -> None:
    chunker = Chunker()
    embedder = EmbeddingGenerator()
    indexer = VectorIndexer()

    for doc in DOCS:
        chunks = chunker.chunk(doc["text"])
        for i, chunk in enumerate(chunks):
            embedding = embedder.embed(chunk)
            metadata = {"title": doc["title"], **doc["metadata"]}
            await indexer.upsert(
                doc_id=doc["doc_id"],
                chunk_index=i,
                content=chunk,
                embedding=embedding,
                metadata=metadata,
            )

    print("Seeded RAG documents")


if __name__ == "__main__":
    asyncio.run(main())
