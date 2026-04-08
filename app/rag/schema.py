from __future__ import annotations

import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from app.db.vector_client import get_vector_engine
from app.rag.constants import EMBEDDING_DIM

logger = logging.getLogger(__name__)

_init_lock = asyncio.Lock()
_initialized = False
_rag_available = True  # set to False if pgvector is not installed


class RagUnavailableError(RuntimeError):
    """Raised when the pgvector extension is not installed on the database."""


async def ensure_rag_schema() -> None:
    global _initialized, _rag_available
    if _initialized:
        if not _rag_available:
            raise RagUnavailableError("pgvector extension is not installed")
        return
    async with _init_lock:
        if _initialized:
            if not _rag_available:
                raise RagUnavailableError("pgvector extension is not installed")
            return
        engine = get_vector_engine()
        try:
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
            _rag_available = True
        except DBAPIError as exc:
            if "vector.control" in str(exc) or "UndefinedFileError" in str(exc) or "vector" in str(exc).lower():
                _rag_available = False
                logger.warning(
                    "pgvector extension is not installed on PostgreSQL. "
                    "RAG search will be disabled. "
                    "To fix: sudo apt-get install -y postgresql-14-pgvector"
                )
                raise RagUnavailableError("pgvector extension is not installed") from exc
            raise
        finally:
            _initialized = True
