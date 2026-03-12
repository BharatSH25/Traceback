from fastapi import FastAPI

from app.api.investigation_api import router as investigation_router
from app.telemetry.logging import configure_logging
from app.config.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title="AI Incident Investigation Assistant")
    app.include_router(investigation_router, prefix="/api")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
