from __future__ import annotations

from sqlalchemy import text

from app.db.vector_client import get_vector_engine
from app.rag.schema import ensure_rag_schema
from app.rag.utils import to_pgvector


class VectorIndexer:
    async def upsert(
        self,
        doc_id: str,
        chunk_index: int,
        content: str,
        embedding: list[float],
        metadata: dict | None = None,
    ) -> None:
        await ensure_rag_schema()
        engine = get_vector_engine()
        meta = metadata or {}
        vector_literal = to_pgvector(embedding)
        async with engine.begin() as conn:
            await conn.execute(
                text(
                    """
                    INSERT INTO rag_documents (doc_id, chunk_index, content, metadata, embedding)
                    VALUES (:doc_id, :chunk_index, :content, :metadata, :embedding::vector)
                    ON CONFLICT (doc_id, chunk_index)
                    DO UPDATE SET
                        content = EXCLUDED.content,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding
                    """
                ),
                {
                    "doc_id": doc_id,
                    "chunk_index": chunk_index,
                    "content": content,
                    "metadata": meta,
                    "embedding": vector_literal,
                },
            )
