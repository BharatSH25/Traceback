from __future__ import annotations

from sqlalchemy import text

from app.db.vector_client import get_vector_engine
from app.rag.schema import ensure_rag_schema
from app.rag.utils import to_pgvector


class VectorSearch:
    async def search(self, embedding: list[float], k: int = 5) -> list[dict]:
        await ensure_rag_schema()
        engine = get_vector_engine()
        vector_literal = to_pgvector(embedding)
        async with engine.begin() as conn:
            result = await conn.execute(
                text(
                    """
                    SELECT content, metadata, (embedding <=> :embedding::vector) AS distance
                    FROM rag_documents
                    ORDER BY embedding <=> :embedding::vector
                    LIMIT :k
                    """
                ),
                {"embedding": vector_literal, "k": k},
            )
            rows = result.fetchall()
        return [
            {"text": r[0], "metadata": r[1], "distance": float(r[2])}
            for r in rows
        ]
