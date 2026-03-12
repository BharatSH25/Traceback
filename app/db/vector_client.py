from app.db.postgres_client import get_engine


def get_vector_engine():
    return get_engine()
