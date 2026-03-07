"""Notification endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import NotificationResponse
from app.notifications.notification_service import NotificationService

router = APIRouter()


@router.get("/", response_model=list[NotificationResponse])
async def list_notifications(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    return await NotificationService.list_notifications(db, skip, limit)


@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
):
    success = await NotificationService.mark_read(db, notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"detail": "Notification marked as read"}
