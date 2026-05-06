from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import UserCreate, UserUpdate, UserResponse, SkillResponse
from src.repository import users as repository_users
from src.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = Query(0, ge=0, description="Кількість записів, які потрібно пропустити (пагінація)"),
    limit: int = Query(100, ge=1, le=500, description="Максимальна кількість записів у відповіді"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати список користувачів."""
    return await repository_users.get_users(skip, limit, db)


@router.get("/me", response_model=UserResponse)
async def read_me(
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),
):
    """Отримати інформацію про поточного авторизованого користувача."""
    user_id, _ = current_user
    user = await repository_users.get_user(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int = Path(..., ge=1, description="Унікальний ідентифікатор користувача"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати інформацію про користувача за його ID."""
    user = await repository_users.get_user(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Створити нового користувача."""
    if await repository_users.get_user_by_email(user.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email вже зареєстрований"
        )
    if await repository_users.get_user_by_username(user.username, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username вже зайнятий"
        )
    return await repository_users.create_user(user, db)


@router.put("/me", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),
):
    """Оновити дані поточного авторизованого користувача."""
    user_id, _ = current_user
    user = await repository_users.update_user(user_id, user_update, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int = Path(..., ge=1, description="Унікальний ідентифікатор користувача, якого потрібно оновити"),
    user_update: UserUpdate = ...,
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),
):
    """Оновити дані користувача (тільки свій профіль або адмін)."""
    current_user_id, role = current_user
    if current_user_id != user_id and role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостатньо прав для редагування цього користувача",
        )
    user = await repository_users.update_user(user_id, user_update, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return user


@router.get("/{user_id}/skills", response_model=List[SkillResponse])
async def read_user_skills(
    user_id: int = Path(..., ge=1, description="Унікальний ідентифікатор користувача, чиї навички потрібно отримати"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати всі навички користувача."""
    skills = await repository_users.get_user_skills(user_id, db)
    if skills is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return skills