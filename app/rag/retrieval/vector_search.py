from __future__ import annotations

import logging

from sqlalchemy import text

from app.db.vector_client import get_vector_engine
from app.rag.schema import RagUnavailableError, ensure_rag_schema
from app.rag.utils import to_pgvector

logger = logging.getLogger(__name__)


class VectorSearch:
    async def search(self, embedding: list[float], k: int = 5) -> list[dict]:
        try:
            await ensure_rag_schema()
        except RagUnavailableError:
            logger.warning("RAG search skipped: pgvector not available.")
            return []

        engine = get_vector_engine()
        async with engine.begin() as conn:
            result = await conn.execute(
                text(
                    """
                    SELECT content, metadata, (embedding <=> CAST(:embedding AS vector)) AS distance
                    FROM rag_documents
                    ORDER BY embedding <=> CAST(:embedding AS vector)
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
