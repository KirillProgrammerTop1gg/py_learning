from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import Animal


async def create_animal_db(db: AsyncSession, data: dict):
    animal = Animal(**data)
    db.add(animal)
    await db.commit()
    await db.refresh(animal)
    return animal


async def get_animal_db(db: AsyncSession, animal_id: int):
    stmt = select(Animal).where(Animal.id == animal_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
