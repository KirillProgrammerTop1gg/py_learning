from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.v2 import AnimalCreateV2, AnimalResponseV2
from services.animals import create_animal_db, get_animal_db

router = APIRouter(prefix="/v2/animals", tags=["v2"])


@router.post("/", response_model=AnimalResponseV2, status_code=201)
async def create_animal_v2(
    animal_data: AnimalCreateV2,
    db: AsyncSession = Depends(get_db),
):
    if animal_data.age <= 0:
        raise HTTPException(status_code=400, detail="Age cannot be negative or zero")

    return await create_animal_db(db, animal_data.model_dump())


@router.get("/{animal_id}", response_model=AnimalResponseV2)
async def get_animal_v2(
    animal_id: int,
    db: AsyncSession = Depends(get_db),
):
    animal = await get_animal_db(db, animal_id)

    if not animal:
        raise HTTPException(404, "Not found")

    return animal
