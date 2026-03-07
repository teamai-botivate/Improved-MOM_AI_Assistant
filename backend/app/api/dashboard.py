"""Dashboard analytics endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import AnalyticsResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/", response_model=AnalyticsResponse)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
):
    return await DashboardService.get_dashboard(db)
