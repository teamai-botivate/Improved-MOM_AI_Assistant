"""Task service – CRUD and status tracking for tasks."""

from datetime import date, datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import Task, TaskHistory, TaskStatus, Meeting
from app.schemas.schemas import TaskCreate, TaskUpdate


class TaskService:

    @staticmethod
    async def create_task(db: AsyncSession, meeting_id: int, data: TaskCreate) -> Task:
        task = Task(
            meeting_id=meeting_id,
            title=data.title,
            description=data.description,
            responsible_person=data.responsible_person,
            responsible_email=data.responsible_email,
            deadline=data.deadline,
            status=data.status,
        )
        db.add(task)
        await db.flush()

        # Initial history entry
        db.add(TaskHistory(
            task_id=task.id,
            previous_status=None,
            new_status=task.status,
            changed_by="system",
        ))
        await db.flush()
        await db.refresh(task)
        return task

    @staticmethod
    async def get_task(db: AsyncSession, task_id: int) -> Task | None:
        result = await db.execute(
            select(Task).options(selectinload(Task.history)).where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_tasks(
        db: AsyncSession,
        meeting_id: int | None = None,
        status: TaskStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        query = select(Task).options(selectinload(Task.meeting))
        if meeting_id:
            query = query.where(Task.meeting_id == meeting_id)
        if status:
            query = query.where(Task.status == status)
        query = query.order_by(Task.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_task(
        db: AsyncSession, task_id: int, data: TaskUpdate, changed_by: str = "system"
    ) -> Task | None:
        task = await TaskService.get_task(db, task_id)
        if not task:
            return None

        old_status = task.status
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Log status change
        if "status" in update_data and update_data["status"] != old_status:
            db.add(TaskHistory(
                task_id=task.id,
                previous_status=old_status,
                new_status=task.status,
                changed_by=changed_by,
            ))

        await db.flush()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int) -> bool:
        task = await TaskService.get_task(db, task_id)
        if not task:
            return False
        await db.delete(task)
        await db.flush()
        return True

    @staticmethod
    async def count_by_status(db: AsyncSession) -> dict[str, int]:
        counts = {}
        for s in TaskStatus:
            result = await db.execute(select(func.count(Task.id)).where(Task.status == s))
            counts[s.value] = result.scalar() or 0
        return counts

    @staticmethod
    async def overdue_tasks(db: AsyncSession) -> list[Task]:
        today = date.today()
        result = await db.execute(
            select(Task)
            .options(selectinload(Task.meeting))
            .where(Task.deadline < today, Task.status != TaskStatus.COMPLETED)
            .order_by(Task.deadline.asc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_task_history(db: AsyncSession, task_id: int) -> list[TaskHistory]:
        result = await db.execute(
            select(TaskHistory)
            .where(TaskHistory.task_id == task_id)
            .order_by(TaskHistory.changed_at.desc())
        )
        return list(result.scalars().all())
