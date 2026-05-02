from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ReviewCreate, ReviewResponse
from src.repository import reviews as repository_reviews

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=List[ReviewResponse])
async def read_reviews(
    skip: int = Query(0, ge=0, description="Кількість записів, які потрібно пропустити (пагінація)"),
    limit: int = Query(100, ge=1, le=500, description="Максимальна кількість записів у відповіді"),
    user_id: Optional[int] = Query(None, ge=1, description="Якщо вказано - повертає лише відгуки про конкретного користувача"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати список відгуків."""
    return await repository_reviews.get_reviews(skip, limit, user_id, db)


@router.get("/{review_id}", response_model=ReviewResponse)
async def read_review(
    review_id: int = Path(..., ge=1, description="Унікальний ідентифікатор відгуку"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати конкретний відгук."""
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
    reviewer_id: int = Query(1, ge=1, description="ID користувача, який залишає відгук (тимчасово, поки немає автентифікації)"),
    db: AsyncSession = Depends(get_db),
):
    """Створити відгук після завершеного обміну."""
    db_review = await repository_reviews.create_review(review, reviewer_id, db)
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не можна створити відгук. Перевірте, чи обмін завершений та чи ви були його учасником",
        )
    return db_review


@router.get("/user/{user_id}", response_model=List[ReviewResponse])
async def read_user_reviews(
    user_id: int = Path(..., ge=1, description="Унікальний ідентифікатор користувача, чиї отримані відгуки потрібно отримати"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати всі відгуки про користувача."""
    return await repository_reviews.get_user_reviews(user_id, db)


@router.get("/user/{user_id}/rating")
async def get_user_rating(
    user_id: int = Path(..., ge=1, description="Унікальний ідентифікатор користувача, чий середній рейтинг потрібно розрахувати"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати середній рейтинг користувача."""
    rating_info = await repository_reviews.get_user_rating(user_id, db)
    if rating_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено",
        )
    return rating_info