"""Task CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.models import TaskStatus
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskHistoryResponse
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    meeting_id: int | None = None,
    status: TaskStatus | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await TaskService.list_tasks(db, meeting_id=meeting_id, status=status, skip=skip, limit=limit)


@router.post("/{meeting_id}", response_model=TaskResponse, status_code=201)
async def create_task(
    meeting_id: int,
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    return await TaskService.create_task(db, meeting_id, data)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    task = await TaskService.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    task = await TaskService.update_task(db, task_id, data, changed_by="system")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await TaskService.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}


@router.get("/{task_id}/history", response_model=list[TaskHistoryResponse])
async def get_task_history(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await TaskService.get_task_history(db, task_id)


@router.get("/overdue/list", response_model=list[TaskResponse])
async def get_overdue_tasks(
    db: AsyncSession = Depends(get_db),
):
    return await TaskService.overdue_tasks(db)
