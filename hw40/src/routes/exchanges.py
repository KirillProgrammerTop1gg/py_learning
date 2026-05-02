from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.db import get_db
from src.schemas import ExchangeCreate, ExchangeUpdate, ExchangeResponse, ExchangeStatus
from src.repository import exchanges as repository_exchanges

router = APIRouter(prefix="/exchanges", tags=["exchanges"])


@router.get("/", response_model=List[ExchangeResponse])
async def read_exchanges(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[ExchangeStatus] = None,
    user_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    return await repository_exchanges.get_exchanges(
        skip, limit, status_filter, user_id, db
    )


@router.get("/my/sent", response_model=List[ExchangeResponse])
async def read_my_sent_exchanges(
    user_id: int = 1, db: AsyncSession = Depends(get_db)
):
    return await repository_exchanges.get_user_sent_exchanges(user_id, db)


@router.get("/my/received", response_model=List[ExchangeResponse])
async def read_my_received_exchanges(
    user_id: int = 1, db: AsyncSession = Depends(get_db)
):
    return await repository_exchanges.get_user_received_exchanges(user_id, db)


@router.get("/{exchange_id}", response_model=ExchangeResponse)
async def read_exchange(exchange_id: int, db: AsyncSession = Depends(get_db)):
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
    sender_id: int = 1,
    db: AsyncSession = Depends(get_db),
):
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
    exchange_id: int,
    exchange_update: ExchangeUpdate,
    current_user_id: int = 1,
    db: AsyncSession = Depends(get_db),
):
    exchange = await repository_exchanges.update_exchange(
        exchange_id, exchange_update, current_user_id, db
    )
    if exchange is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Обмін з ID {exchange_id} не знайдено або недостатньо прав",
        )
    return exchange