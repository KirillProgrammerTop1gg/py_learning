from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import stats as repository_stats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/top-skills")
async def top_skills(
    limit: int = Query(10, ge=1, le=100, description="Кількість навичок у відповіді"),
    db: AsyncSession = Depends(get_db),
):
    """Топ популярних навичок за кількістю користувачів."""
    return await repository_stats.get_top_skills(db, limit)


@router.get("/active-users")
async def active_users(
    limit: int = Query(10, ge=1, le=100, description="Кількість користувачів у відповіді"),
    db: AsyncSession = Depends(get_db),
):
    """Найактивніші користувачі за сумарною активністю (надіслані + отримані обміни + залишені відгуки)."""
    return await repository_stats.get_active_users(db, limit)


@router.get("/exchange-success-rate")
async def exchange_success_rate(db: AsyncSession = Depends(get_db)):
    """Загальна статистика обмінів: відсоток успішних, відсоток невдалих, розбивка по статусах."""
    return await repository_stats.get_exchange_success_rate(db)