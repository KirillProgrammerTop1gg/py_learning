from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text
import asyncio
from typing import AsyncGenerator


# 1. URL бази даних. Зверніть увагу на "+aiosqlite" — це вказівка на асинхронний драйвер.
DATABASE_URL = "sqlite+aiosqlite:///./restaurant.db"

# 2. Створюємо Двигун. echo=True виводить згенерований SQL у консоль (корисно для навчання)
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. Фабрика сесій (Sessionmaker).
# Ми вчимо її створювати саме асинхронні сесії (class_=AsyncSession)
async_session_factory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False  # КРИТИЧНО ДЛЯ ASYNC!
)


# 4. Базовий клас. Це "матриця", з якої будуть зліплені всі наші таблиці
class Base(DeclarativeBase):
    pass


class Dish(Base):
    # Явно вказуємо назву таблиці в SQL
    __tablename__ = "dishes"

    # Mapped[int] — це підказка для Python (це число)
    # mapped_column(...) — це інструкція для бази даних (це первинний ключ)
    id: Mapped[int] = mapped_column(primary_key=True)

    # String(100) обмежує довжину в базі даних (VARCHAR 100)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    price: Mapped[float] = mapped_column()

    # Mapped[str | None] каже Python, що тут може бути рядок або Нічого.
    # mapped_column автоматично робить це поле NULLABLE у базі даних.
    description: Mapped[str | None] = mapped_column(Text)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # async with автоматично викликає .close() при виході з блоку
    async with async_session_factory() as session:
        # yield призупиняє функцію і віддає сесію у ваш маршрут (роздає окуляри)
        yield session
        # ... маршрут обробляє запит користувача ...
        # Коли маршрут закінчив роботу, код продовжується звідси,
        # і async with безпечно закриває підключення (забирає окуляри).


if __name__ == "__main__":
    asyncio.run(create_db())