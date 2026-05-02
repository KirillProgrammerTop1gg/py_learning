from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.db import get_db
from src.schemas import UserCreate, UserUpdate, UserResponse, SkillResponse
from src.repository import users as repository_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Отримати список користувачів.

    - **skip**: кількість записів, які потрібно пропустити
    - **limit**: максимальна кількість записів у відповіді
    """
    return await repository_users.get_users(skip, limit, db)


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Отримати інформацію про користувача за його ID.

    - **user_id**: унікальний ідентифікатор користувача
    """
    user = await repository_users.get_user(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Створити нового користувача.

    - **user**: дані нового користувача (email, username, пароль тощо)
    """
    if await repository_users.get_user_by_email(user.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email вже зареєстрований"
        )

    if await repository_users.get_user_by_username(user.username, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username вже зайнятий"
        )

    return await repository_users.create_user(user, db)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Оновити дані користувача.

    - **user_id**: унікальний ідентифікатор користувача
    - **user_update**: поля, які потрібно оновити
    """
    user = await repository_users.update_user(user_id, user_update, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return user


@router.get("/{user_id}/skills", response_model=List[SkillResponse])
async def read_user_skills(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Отримати всі навички користувача.

    - **user_id**: унікальний ідентифікатор користувача
    """
    skills = await repository_users.get_user_skills(user_id, db)
    if skills is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return skills
