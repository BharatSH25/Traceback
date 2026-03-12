from fastapi import APIRouter

from app.models.request_models import InvestigationRequest
from app.models.response_models import RootCauseReport
from app.services.investigation_service import InvestigationService

router = APIRouter()
service = InvestigationService()


@router.post("/investigate", response_model=RootCauseReport)
async def investigate(req: InvestigationRequest) -> RootCauseReport:
    return await service.investigate(req)
