"""
conftest.py — спільні фікстури для всіх тестових модулів.

Стратегія:
- Використовуємо SQLite (aiosqlite) замість PostgreSQL — без зовнішніх залежностей.
- Кожен тест отримує свіжу БД через rollback після завершення.
- AsyncClient підключається до FastAPI через ASGI-транспорт.

Встановлення залежностей:
    pip install pytest pytest-asyncio httpx aiosqlite
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.database.db import Base, get_db
from src.database.models import (
    Category,
    User,
    Skill,
    Exchange,
    Review,
    SkillLevel,
    ExchangeStatus,
)
from main import app

# ─────────────────────── Engine ──────────────────────────────────────────────

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ─────────────────────── Схема (один раз на весь run) ────────────────────────


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ─────────────────────── DB-сесія (ізольована на кожен тест) ─────────────────


@pytest_asyncio.fixture
async def db_session():
    """Кожен тест отримує чисту БД через rollback."""
    async with engine.connect() as conn:
        await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            yield session
        finally:
            await session.close()
            await conn.rollback()


# ─────────────────────── HTTP-клієнт ─────────────────────────────────────────


@pytest_asyncio.fixture
async def client(db_session):
    """AsyncClient з підміненою залежністю get_db."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


# ─────────────────────── Seed-фікстури ───────────────────────────────────────


@pytest_asyncio.fixture
async def category(db_session):
    cat = Category(
        name="Програмування",
        slug="programming",
        description="Мови програмування, фреймворки",
        icon="code",
        is_active=True,
    )
    db_session.add(cat)
    await db_session.commit()
    await db_session.refresh(cat)
    return cat


@pytest_asyncio.fixture
async def category2(db_session):
    cat = Category(
        name="Музика",
        slug="music",
        description="Гра на інструментах",
        icon="music",
        is_active=True,
    )
    db_session.add(cat)
    await db_session.commit()
    await db_session.refresh(cat)
    return cat


@pytest_asyncio.fixture
async def inactive_category(db_session):
    cat = Category(
        name="Архів",
        slug="archive",
        description="Неактивна",
        is_active=False,
    )
    db_session.add(cat)
    await db_session.commit()
    await db_session.refresh(cat)
    return cat


@pytest_asyncio.fixture
async def user_a(db_session):
    u = User(username="alice", email="alice@test.com", full_name="Alice A")
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)
    return u


@pytest_asyncio.fixture
async def user_b(db_session):
    u = User(username="bob", email="bob@test.com", full_name="Bob B")
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)
    return u


@pytest_asyncio.fixture
async def skill(db_session, category, user_a):
    s = Skill(
        title="Python basics",
        description="Основи Python для початківців",
        category_id=category.id,
        level=SkillLevel.beginner,
        can_teach=True,
        want_learn=False,
    )
    db_session.add(s)
    await db_session.commit()
    await db_session.refresh(s)
    user_a.skills.append(s)
    await db_session.commit()
    return s


@pytest_asyncio.fixture
async def skill2(db_session, category2, user_b):
    s = Skill(
        title="Гітара для початківців",
        description="Навчу грати на гітарі з нуля",
        category_id=category2.id,
        level=SkillLevel.intermediate,
        can_teach=True,
        want_learn=False,
    )
    db_session.add(s)
    await db_session.commit()
    await db_session.refresh(s)
    return s


@pytest_asyncio.fixture
async def exchange_pending(db_session, user_a, user_b, skill):
    ex = Exchange(
        sender_id=user_a.id,
        receiver_id=user_b.id,
        skill_id=skill.id,
        message="Давай обміняємось!",
        hours_proposed=3,
        status=ExchangeStatus.pending,
    )
    db_session.add(ex)
    await db_session.commit()
    await db_session.refresh(ex)
    return ex


@pytest_asyncio.fixture
async def exchange_completed(db_session, user_a, user_b, skill):
    ex = Exchange(
        sender_id=user_a.id,
        receiver_id=user_b.id,
        skill_id=skill.id,
        message="Завершений обмін",
        hours_proposed=2,
        status=ExchangeStatus.completed,
    )
    db_session.add(ex)
    await db_session.commit()
    await db_session.refresh(ex)
    return ex


@pytest_asyncio.fixture
async def review(db_session, exchange_completed, user_a, user_b):
    r = Review(
        exchange_id=exchange_completed.id,
        reviewer_id=user_a.id,
        reviewed_id=user_b.id,
        rating=5,
        comment="Чудово!",
    )
    db_session.add(r)
    await db_session.commit()
    await db_session.refresh(r)
    return r
