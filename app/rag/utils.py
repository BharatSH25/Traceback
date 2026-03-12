from __future__ import annotations


def to_pgvector(values: list[float]) -> str:
    # pgvector expects a string like "[0.1,0.2,0.3]"
    return "[" + ",".join(f"{v:.6f}" for v in values) + "]"

# Need to implement interface for different vectordb's
def to_pinecone(values: list[float]):
    #TODO : to implement pincone
    return values
