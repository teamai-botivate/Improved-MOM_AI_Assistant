"""Scheduled background jobs for reminders and warnings."""

import asyncio
import logging
from datetime import date, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.session import async_session_factory
from app.services.task_service import TaskService
from app.services.attendance_service import AttendanceService
from app.notifications.notification_service import NotificationService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def check_deadline_reminders():
    """Send reminders for tasks due within 2 days."""
    logger.info("Running deadline reminder check")
    async with async_session_factory() as db:
        try:
            from sqlalchemy import select
            from app.models.models import Task, TaskStatus
            tomorrow = date.today() + timedelta(days=1)
            day_after = date.today() + timedelta(days=2)
            result = await db.execute(
                select(Task).where(
                    Task.deadline.between(tomorrow, day_after),
                    Task.status != TaskStatus.COMPLETED,
                )
            )
            tasks = result.scalars().all()
            for task in tasks:
                await NotificationService.notify_deadline_reminder(db, task)
            await db.commit()
            logger.info("Deadline reminders sent for %d tasks", len(tasks))
        except Exception as e:
            logger.error("Deadline reminder check failed: %s", e)
            await db.rollback()


async def check_overdue_tasks():
    """Send alerts for overdue tasks."""
    logger.info("Running overdue task check")
    async with async_session_factory() as db:
        try:
            overdue = await TaskService.overdue_tasks(db)
            for task in overdue:
                await NotificationService.notify_overdue(db, task)
            await db.commit()
            logger.info("Overdue alerts sent for %d tasks", len(overdue))
        except Exception as e:
            logger.error("Overdue check failed: %s", e)
            await db.rollback()


async def check_frequent_absentees():
    """Warn about users who have been absent 3+ times."""
    logger.info("Running absentee check")
    async with async_session_factory() as db:
        try:
            absentees = await AttendanceService.get_frequent_absentees(db)
            for record in absentees:
                if record.get("email"):
                    await NotificationService.notify_absence_warning(
                        db,
                        email=record["email"],
                        user_name=record["user_name"],
                        count=record["absent_count"],
                    )
            await db.commit()
            logger.info("Absence warnings sent for %d users", len(absentees))
        except Exception as e:
            logger.error("Absentee check failed: %s", e)
            await db.rollback()


def start_scheduler():
    """Start the APScheduler with configured jobs."""
    scheduler.add_job(check_deadline_reminders, "cron", hour=9, minute=0, id="deadline_reminders")
    scheduler.add_job(check_overdue_tasks, "cron", hour=10, minute=0, id="overdue_tasks")
    scheduler.add_job(check_frequent_absentees, "cron", day_of_week="mon", hour=8, minute=0, id="absentee_check")
    scheduler.start()
    logger.info("Background scheduler started")


def shutdown_scheduler():
    """Shut down the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Background scheduler stopped")
