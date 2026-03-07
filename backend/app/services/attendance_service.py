"""Attendance service – tracking and absentee warnings."""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Attendee, AttendanceStatus


class AttendanceService:

    ABSENT_WARNING_THRESHOLD = 3

    @staticmethod
    async def get_attendance_for_meeting(db: AsyncSession, meeting_id: int) -> list[Attendee]:
        result = await db.execute(
            select(Attendee).where(Attendee.meeting_id == meeting_id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_frequent_absentees(db: AsyncSession, threshold: int | None = None) -> list[dict]:
        """Return users who have been absent >= threshold times."""
        t = threshold or AttendanceService.ABSENT_WARNING_THRESHOLD
        result = await db.execute(
            select(
                Attendee.user_name,
                Attendee.email,
                func.count(Attendee.id).label("absent_count"),
            )
            .where(Attendee.attendance_status == AttendanceStatus.ABSENT)
            .group_by(Attendee.user_name, Attendee.email)
            .having(func.count(Attendee.id) >= t)
        )
        return [
            {"user_name": row[0], "email": row[1], "absent_count": row[2]}
            for row in result.all()
        ]

    @staticmethod
    async def get_user_attendance_count(db: AsyncSession, user_name: str) -> dict:
        present = await db.execute(
            select(func.count(Attendee.id))
            .where(Attendee.user_name == user_name, Attendee.attendance_status == AttendanceStatus.PRESENT)
        )
        absent = await db.execute(
            select(func.count(Attendee.id))
            .where(Attendee.user_name == user_name, Attendee.attendance_status == AttendanceStatus.ABSENT)
        )
        return {
            "user_name": user_name,
            "present": present.scalar() or 0,
            "absent": absent.scalar() or 0,
        }
