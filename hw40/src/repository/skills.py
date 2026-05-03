from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, or_

from src.database.models import Skill, User, Category
from src.schemas import SkillCreate, SkillUpdate


def _skill_load_options():
    return [
        selectinload(Skill.users),
        selectinload(Skill.category),
    ]


async def get_skills(
    skip: int,
    limit: int,
    category_id: Optional[int],
    can_teach: Optional[bool],
    want_learn: Optional[bool],
    search: Optional[str],
    db: AsyncSession,
) -> List[Skill]:
    """Отримати список навичок з фільтрацією та пагінацією."""
    stmt = select(Skill).options(*_skill_load_options())

    if category_id is not None:
        stmt = stmt.where(Skill.category_id == category_id)
    if can_teach is not None:
        stmt = stmt.where(Skill.can_teach == can_teach)
    if want_learn is not None:
        stmt = stmt.where(Skill.want_learn == want_learn)
    if search:
        search_filter = f"%{search}%"
        stmt = stmt.where(
            or_(
                Skill.title.ilike(search_filter),
                Skill.description.ilike(search_filter),
            )
        )

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_skill(skill_id: int, db: AsyncSession) -> Optional[Skill]:
    """Отримати навичку за ID."""
    stmt = select(Skill).options(*_skill_load_options()).where(Skill.id == skill_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_skill(skill: SkillCreate, user_id: int, db: AsyncSession) -> Skill:
    """Створити навичку та прив'язати до користувача."""
    # Перевірка що категорія існує
    category = await db.get(Category, skill.category_id)
    if not category:
        raise ValueError(f"Категорія з ID {skill.category_id} не знайдена")
    if not category.is_active:
        raise ValueError(f"Категорія '{category.name}' неактивна")

    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    await db.commit()
    await db.refresh(db_skill)

    user = await db.get(User, user_id)
    if user:
        user.skills.append(db_skill)
        await db.commit()

    stmt = select(Skill).options(*_skill_load_options()).where(Skill.id == db_skill.id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def update_skill(
    skill_id: int, skill_update: SkillUpdate, db: AsyncSession
) -> Optional[Skill]:
    """Оновити існуючу навичку."""
    stmt = select(Skill).options(*_skill_load_options()).where(Skill.id == skill_id)
    result = await db.execute(stmt)
    db_skill = result.scalar_one_or_none()
    if not db_skill:
        return None

    update_data = skill_update.model_dump(exclude_unset=True)

    # Якщо змінюється category_id — перевіряємо що вона існує і активна
    if "category_id" in update_data:
        category = await db.get(Category, update_data["category_id"])
        if not category:
            raise ValueError(f"Категорія з ID {update_data['category_id']} не знайдена")
        if not category.is_active:
            raise ValueError(f"Категорія '{category.name}' неактивна")

    for field, value in update_data.items():
        setattr(db_skill, field, value)

    await db.commit()
    await db.refresh(db_skill)
    return db_skill


async def delete_skill(skill_id: int, db: AsyncSession) -> Optional[Skill]:
    """Видалити навичку."""
    stmt = select(Skill).where(Skill.id == skill_id)
    result = await db.execute(stmt)
    db_skill = result.scalar_one_or_none()
    if db_skill:
        await db.delete(db_skill)
        await db.commit()
    return db_skill


async def find_skill_matches(skill_id: int, db: AsyncSession) -> dict:
    """Знайти відповідності для обміну навичками в межах тієї ж категорії."""
    stmt = select(Skill).options(*_skill_load_options()).where(Skill.id == skill_id)
    result = await db.execute(stmt)
    skill = result.scalar_one_or_none()
    if not skill:
        return {"skill": None, "matches": []}

    stmt = (
        select(Skill)
        .options(*_skill_load_options())
        .where(
            Skill.id != skill_id,
            Skill.category_id == skill.category_id,
            Skill.title.ilike(f"%{skill.title}%"),
        )
    )
    result = await db.execute(stmt)
    similar_skills = result.scalars().all()

    matches = []
    for other_skill in similar_skills:
        if skill.want_learn and other_skill.can_teach:
            matches.append(
                {"type": "teacher", "skill": other_skill, "users": other_skill.users}
            )
        elif skill.can_teach and other_skill.want_learn:
            matches.append(
                {"type": "student", "skill": other_skill, "users": other_skill.users}
            )

    return {"skill": skill, "matches_count": len(matches), "matches": matches}
