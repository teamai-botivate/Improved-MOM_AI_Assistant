"""User service – CRUD operations for users."""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:

    @staticmethod
    async def create_user(db: AsyncSession, data: UserCreate) -> User:
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password),
            role=data.role,
            phone=data.phone,
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
        result = await db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, data: UserUpdate) -> User | None:
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return False
        await db.delete(user)
        await db.flush()
        return True

    @staticmethod
    async def count_users(db: AsyncSession) -> int:
        result = await db.execute(select(func.count(User.id)))
        return result.scalar() or 0
