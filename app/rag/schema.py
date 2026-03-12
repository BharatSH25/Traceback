from __future__ import annotations

import asyncio

from sqlalchemy import text

from app.db.vector_client import get_vector_engine
from app.rag.constants import EMBEDDING_DIM


_init_lock = asyncio.Lock()
_initialized = False


async def ensure_rag_schema() -> None:
    global _initialized
    if _initialized:
        return
    async with _init_lock:
        if _initialized:
            return
        engine = get_vector_engine()
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
            await conn.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS rag_documents (
                        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                        doc_id text NOT NULL,
                        chunk_index int NOT NULL,
                        content text NOT NULL,
                        metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
                        embedding vector(:dim) NOT NULL,
                        created_at timestamptz NOT NULL DEFAULT now(),
                        UNIQUE (doc_id, chunk_index)
                    )
                    """
                ).bindparams(dim=EMBEDDING_DIM)
            )
            await conn.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS rag_documents_embedding_idx
                    ON rag_documents USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100)
                    """
                )
            )
        _initialized = True
