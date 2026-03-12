from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.config.settings import get_settings


_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(settings.database_url)
    return _engine
