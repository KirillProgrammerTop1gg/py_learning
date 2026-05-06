from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ExchangeCreate, ExchangeUpdate, ExchangeResponse, ExchangeStatus
from src.repository import exchanges as repository_exchanges
from src.auth import get_current_user

router = APIRouter(prefix="/exchanges", tags=["exchanges"])


@router.get("/", response_model=List[ExchangeResponse])
async def read_exchanges(
    skip: int = Query(0, ge=0, description="Кількість записів, які потрібно пропустити (пагінація)"),
    limit: int = Query(100, ge=1, le=500, description="Максимальна кількість записів у відповіді"),
    status_filter: Optional[ExchangeStatus] = Query(None, description="Фільтр за статусом обміну"),
    user_id: Optional[int] = Query(None, ge=1, description="Повертає лише обміни вказаного користувача"),
    from_date: Optional[datetime] = Query(None, description="Фільтр від дати (ISO 8601)"),
    to_date: Optional[datetime] = Query(None, description="Фільтр до дати (ISO 8601)"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Сортування: asc або desc"),
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),
):
    """Отримати список обмінів з фільтрацією та сортуванням."""
    if from_date and to_date and from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="from_date не може бути пізніше за to_date",
        )
    return await repository_exchanges.get_exchanges(
        skip, limit, status_filter, user_id, from_date, to_date, sort_order, db
    )


@router.get("/my/sent", response_model=List[ExchangeResponse])
async def read_my_sent_exchanges(
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),  # user_id береться з токена
):
    """Отримати надіслані запити на обмін поточного користувача."""
    user_id, _ = current_user
    return await repository_exchanges.get_user_sent_exchanges(user_id, db)


@router.get("/my/received", response_model=List[ExchangeResponse])
async def read_my_received_exchanges(
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),  # user_id береться з токена
):
    """Отримати отримані запити на обмін поточного користувача."""
    user_id, _ = current_user
    return await repository_exchanges.get_user_received_exchanges(user_id, db)


@router.get("/{exchange_id}", response_model=ExchangeResponse)
async def read_exchange(
    exchange_id: int = Path(..., ge=1, description="Унікальний ідентифікатор обміну"),
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),
):
    """Отримати деталі обміну за ID."""
    exchange = await repository_exchanges.get_exchange(exchange_id, db)
    if exchange is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Обмін з ID {exchange_id} не знайдено",
        )
    return exchange


@router.post("/", response_model=ExchangeResponse, status_code=status.HTTP_201_CREATED)
async def create_exchange(
    exchange: ExchangeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),  # sender_id береться з токена
):
    """Створити запит на обмін навичками."""
    sender_id, _ = current_user
    if sender_id == exchange.receiver_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не можна створити обмін з самим собою",
        )
    result = await repository_exchanges.create_exchange(exchange, sender_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Відправника, отримувача або навичку не знайдено",
        )
    return result


@router.put("/{exchange_id}", response_model=ExchangeResponse)
async def update_exchange_status(
    exchange_id: int = Path(..., ge=1, description="Унікальний ідентифікатор обміну"),
    exchange_update: ExchangeUpdate = ...,
    db: AsyncSession = Depends(get_db),
    current_user: tuple = Depends(get_current_user),  # current_user_id береться з токена
):
    """Оновити статус обміну (прийняти, відхилити, скасувати)."""
    current_user_id, _ = current_user
    exchange = await repository_exchanges.update_exchange(
        exchange_id, exchange_update, current_user_id, db
    )
    if exchange is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Обмін з ID {exchange_id} не знайдено або недостатньо прав",
        )
    return exchange