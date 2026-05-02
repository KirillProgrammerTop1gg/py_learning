from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.database.models import Category, Skill
from src.schemas import CategoryCreate, CategoryUpdate


async def get_categories(
    skip: int,
    limit: int,
    only_active: bool,
    db: AsyncSession,
) -> List[Category]:
    """Отримати список категорій з пагінацією."""
    stmt = select(Category)
    if only_active:
        stmt = stmt.where(Category.is_active == True)
    stmt = stmt.order_by(Category.name).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_category(category_id: int, db: AsyncSession) -> Optional[Category]:
    """Отримати категорію за ID."""
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_category_by_slug(slug: str, db: AsyncSession) -> Optional[Category]:
    """Отримати категорію за slug."""
    stmt = select(Category).where(Category.slug == slug)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_category_by_name(name: str, db: AsyncSession) -> Optional[Category]:
    """Отримати категорію за назвою."""
    stmt = select(Category).where(Category.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_category(category: CategoryCreate, db: AsyncSession) -> Category:
    """Створити нову категорію."""
    db_category = Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def update_category(
    category_id: int, category_update: CategoryUpdate, db: AsyncSession
) -> Optional[Category]:
    """Оновити категорію."""
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    db_category = result.scalar_one_or_none()
    if db_category:
        update_data = category_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        await db.commit()
        await db.refresh(db_category)
    return db_category


async def delete_category(category_id: int, db: AsyncSession) -> Optional[Category]:
    """
    Видалити категорію.
    Повертає None якщо категорія не існує,
    підіймає ValueError якщо до неї прив'язані навички.
    """
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    db_category = result.scalar_one_or_none()
    if not db_category:
        return None

    # Перевірка: чи є навички в цій категорії
    count_stmt = select(func.count(Skill.id)).where(Skill.category_id == category_id)
    count_result = await db.execute(count_stmt)
    skills_count = count_result.scalar()
    if skills_count > 0:
        raise ValueError(
            f"Неможливо видалити категорію: до неї прив'язано {skills_count} навичок. "
            "Спочатку перенесіть або видаліть навички."
        )

    await db.delete(db_category)
    await db.commit()
    return db_category


async def get_category_with_skills(
    category_id: int, db: AsyncSession
) -> Optional[Category]:
    """Отримати категорію разом з її навичками."""
    stmt = (
        select(Category)
        .options(selectinload(Category.skills).selectinload(Skill.users))
        .where(Category.id == category_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_skills_count_per_category(
    category_id: int, db: AsyncSession
) -> int:
    """Порахувати кількість навичок у категорії."""
    stmt = select(func.count(Skill.id)).where(Skill.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar() or 0