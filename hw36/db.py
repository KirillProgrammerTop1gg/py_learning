from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text
import asyncio
from typing import AsyncGenerator

# simpler but not async
# DATABASE_URL = "sqlite+aiosqlite:///./eventParticipants.db"
# engine = create_async_engine(DATABASE_URL, echo=True)

# harder but full async
DATABASE_URL = "postgresql+asyncpg://myuser:qwerty@localhost:5432/event_db"
engine = create_async_engine(DATABASE_URL, echo=True, pool_size=10, max_overflow=20)

async_session_factory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    event: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column()


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


if __name__ == "__main__":
    asyncio.run(create_db())
