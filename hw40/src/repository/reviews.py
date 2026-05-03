from typing import List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Review, Exchange, ExchangeStatus as DBExchangeStatus
from src.schemas import ReviewCreate


def _review_load_options():
    return [
        selectinload(Review.reviewer),
        selectinload(Review.reviewed),
    ]


async def get_reviews(
    skip: int,
    limit: int,
    user_id: Optional[int],
    db: AsyncSession,
) -> List[Review]:
    """Отримати список відгуків."""
    stmt = select(Review).options(*_review_load_options())

    if user_id:
        stmt = stmt.where(Review.reviewed_id == user_id)

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_review(review_id: int, db: AsyncSession) -> Optional[Review]:
    """Отримати відгук за ID."""
    stmt = select(Review).options(*_review_load_options()).where(Review.id == review_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_review(review, reviewer_id: int, db):
    stmt = (
        select(Exchange)
        .where(Exchange.id == review.exchange_id)
        .options(
            selectinload(Exchange.sender),
            selectinload(Exchange.receiver),
            selectinload(Exchange.reviews),
        )
    )
    result = await db.execute(stmt)
    exchange = result.scalar_one_or_none()

    if exchange is None:
        return None

    if exchange.status != DBExchangeStatus.completed:
        return None

    if reviewer_id == exchange.sender_id:
        reviewed_id = exchange.receiver_id
    elif reviewer_id == exchange.receiver_id:
        reviewed_id = exchange.sender_id
    else:
        return None

    duplicate_stmt = select(Review).where(
        Review.exchange_id == review.exchange_id,
        Review.reviewer_id == reviewer_id,
    )
    duplicate_result = await db.execute(duplicate_stmt)
    duplicate = duplicate_result.scalar_one_or_none()

    if duplicate is not None:
        return None

    db_review = Review(
        exchange_id=review.exchange_id,
        reviewer_id=reviewer_id,
        reviewed_id=reviewed_id,
        rating=review.rating,
        comment=review.comment,
    )

    db.add(db_review)
    await db.commit()

    stmt = (
        select(Review)
        .where(Review.id == db_review.id)
        .options(
            selectinload(Review.reviewer),
            selectinload(Review.reviewed),
        )
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_user_reviews(user_id: int, db: AsyncSession) -> List[Review]:
    """Отримати всі відгуки про користувача."""
    stmt = (
        select(Review)
        .options(*_review_load_options())
        .where(Review.reviewed_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_rating(user_id: int, db: AsyncSession) -> Optional[dict]:
    """Розрахувати середній рейтинг користувача."""
    stmt = select(
        func.avg(Review.rating).label("average_rating"),
        func.count(Review.id).label("total_reviews"),
    ).where(Review.reviewed_id == user_id)
    result = await db.execute(stmt)
    row = result.first()

    if row and row.total_reviews > 0:
        return {
            "user_id": user_id,
            "average_rating": round(float(row.average_rating), 2),
            "total_reviews": row.total_reviews,
        }

    return {"user_id": user_id, "average_rating": 0, "total_reviews": 0}
