"""Attendance tracking endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import AttendeeResponse
from app.services.attendance_service import AttendanceService

router = APIRouter()


@router.get("/meeting/{meeting_id}", response_model=list[AttendeeResponse])
async def get_meeting_attendance(
    meeting_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await AttendanceService.get_attendance_for_meeting(db, meeting_id)


@router.get("/absentees")
async def get_frequent_absentees(
    threshold: int = 3,
    db: AsyncSession = Depends(get_db),
):
    return await AttendanceService.get_frequent_absentees(db, threshold)


@router.get("/user/{user_name}")
async def get_user_attendance(
    user_name: str,
    db: AsyncSession = Depends(get_db),
):
    return await AttendanceService.get_user_attendance_count(db, user_name)
