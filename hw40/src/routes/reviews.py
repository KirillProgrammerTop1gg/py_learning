from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.db import get_db
from src.schemas import ReviewCreate, ReviewResponse
from src.repository import reviews as repository_reviews

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=List[ReviewResponse])
async def read_reviews(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Отримати список відгуків.

    - **skip**: кількість записів, які потрібно пропустити
    - **limit**: максимальна кількість записів у відповіді
    - **user_id**: якщо вказано, повертає лише відгуки про конкретного користувача
    """
    reviews = await repository_reviews.get_reviews(skip, limit, user_id, db)
    return reviews


@router.get("/{review_id}", response_model=ReviewResponse)
async def read_review(review_id: int, db: AsyncSession = Depends(get_db)):
    """
    Отримати конкретний відгук.

    - **review_id**: унікальний ідентифікатор відгуку
    """
    review = await repository_reviews.get_review(review_id, db)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Відгук з ID {review_id} не знайдено",
        )
    return review


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    reviewer_id: int = 1,  # Тимчасово
    db: AsyncSession = Depends(get_db),
):
    """
    Створити відгук після завершеного обміну.

    - **review**: дані відгуку (текст, рейтинг, ID обміну)
    - **reviewer_id**: ідентифікатор користувача, який залишає відгук
    """
    db_review = await repository_reviews.create_review(review, reviewer_id, db)
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не можна створити відгук. Перевірте, чи обмін завершений та чи ви були його учасником",
        )
    return db_review


@router.get("/user/{user_id}", response_model=List[ReviewResponse])
async def read_user_reviews(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Отримати всі відгуки про користувача.

    - **user_id**: унікальний ідентифікатор користувача
    """
    reviews = await repository_reviews.get_user_reviews(user_id, db)
    return reviews


@router.get("/user/{user_id}/rating")
async def get_user_rating(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Отримати середній рейтинг користувача.

    - **user_id**: унікальний ідентифікатор користувача
    """
    rating_info = await repository_reviews.get_user_rating(user_id, db)
    if rating_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return rating_info
