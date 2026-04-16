from __future__ import annotations

import hashlib

from app.rag.constants import EMBEDDING_DIM


class EmbeddingGenerator:
    def embed(self, text: str) -> list[float]:
        # Deterministic local embedding to keep the pipeline functional without external calls.
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = []
        for i in range(EMBEDDING_DIM):
            b = digest[i % len(digest)]
            values.append((b / 255.0) * 2.0 - 1.0)
        return values
