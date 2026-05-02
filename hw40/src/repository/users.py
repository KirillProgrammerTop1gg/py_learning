from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.models import User
from src.database.db import get_db
from src.schemas import UserCreate, UserUpdate


async def get_users(skip: int, limit: int, db: AsyncSession) -> List[User]:
    """Отримати список користувачів з пагінацією."""
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user(user_id: int, db: AsyncSession) -> Optional[User]:
    """Отримати користувача за його ID."""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(email: str, db: AsyncSession) -> Optional[User]:
    """Отримати користувача за email."""
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_username(username: str, db: AsyncSession) -> Optional[User]:
    """Отримати користувача за username."""
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(user: UserCreate, db: AsyncSession) -> User:
    """Створити нового користувача."""
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(
    user_id: int, user_update: UserUpdate, db: AsyncSession
) -> Optional[User]:
    """Оновити дані користувача."""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def get_user_skills(user_id: int, db: AsyncSession) -> Optional[List]:
    """Отримати всі навички користувача за ID."""
    stmt = (
        select(User)
        .options(selectinload(User.skills))
        .where(User.id == user_id)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user.skills if user else None