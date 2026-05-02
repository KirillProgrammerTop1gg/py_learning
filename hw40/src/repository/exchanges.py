from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from src.database.models import Exchange, User, Skill
from src.schemas import ExchangeCreate, ExchangeUpdate, ExchangeStatus


def _exchange_load_options():
    """selectinload для всіх вкладених relations у ExchangeResponse."""
    return [
        selectinload(Exchange.sender),
        selectinload(Exchange.receiver),
        selectinload(Exchange.skill).selectinload(Skill.users),
    ]


async def get_exchanges(
    skip: int,
    limit: int,
    status_filter: Optional[ExchangeStatus],
    user_id: Optional[int],
    db: AsyncSession,
) -> List[Exchange]:
    """Отримати список обмінів з фільтрацією."""
    stmt = select(Exchange).options(*_exchange_load_options())

    if status_filter:
        stmt = stmt.where(Exchange.status == status_filter.value)
    if user_id:
        stmt = stmt.where(
            or_(Exchange.sender_id == user_id, Exchange.receiver_id == user_id)
        )

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_exchange(exchange_id: int, db: AsyncSession) -> Optional[Exchange]:
    """Отримати обмін за ID."""
    stmt = (
        select(Exchange)
        .options(*_exchange_load_options())
        .where(Exchange.id == exchange_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_exchange(
    exchange: ExchangeCreate, sender_id: int, db: AsyncSession
) -> Optional[Exchange]:
    """Створити новий запит на обмін."""
    sender = await db.get(User, sender_id)
    receiver = await db.get(User, exchange.receiver_id)
    skill = await db.get(Skill, exchange.skill_id)

    if not all([sender, receiver, skill]):
        return None

    db_exchange = Exchange(
        sender_id=sender_id,
        receiver_id=exchange.receiver_id,
        skill_id=exchange.skill_id,
        message=exchange.message,
        hours_proposed=exchange.hours_proposed,
        status=ExchangeStatus.pending.value,
    )

    db.add(db_exchange)
    await db.commit()
    await db.refresh(db_exchange)

    # Перезавантажуємо з усіма relations для серіалізації
    return await get_exchange(db_exchange.id, db)


async def update_exchange(
    exchange_id: int,
    exchange_update: ExchangeUpdate,
    current_user_id: int,
    db: AsyncSession,
) -> Optional[Exchange]:
    """Оновити статус обміну."""
    stmt = select(Exchange).where(Exchange.id == exchange_id)
    result = await db.execute(stmt)
    db_exchange = result.scalar_one_or_none()

    if not db_exchange:
        return None

    if exchange_update.status in [ExchangeStatus.accepted, ExchangeStatus.rejected]:
        if db_exchange.receiver_id != current_user_id:
            return None
    elif exchange_update.status == ExchangeStatus.cancelled:
        if current_user_id not in [db_exchange.sender_id, db_exchange.receiver_id]:
            return None

    db_exchange.status = exchange_update.status.value
    if exchange_update.message:
        db_exchange.message = exchange_update.message

    await db.commit()

    return await get_exchange(exchange_id, db)


async def get_user_sent_exchanges(user_id: int, db: AsyncSession) -> List[Exchange]:
    """Отримати надіслані користувачем запити."""
    stmt = (
        select(Exchange)
        .options(*_exchange_load_options())
        .where(Exchange.sender_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_received_exchanges(user_id: int, db: AsyncSession) -> List[Exchange]:
    """Отримати отримані користувачем запити."""
    stmt = (
        select(Exchange)
        .options(*_exchange_load_options())
        .where(Exchange.receiver_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()