from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.v1 import AnimalCreateV1, AnimalResponseV1
from services.animals import create_animal_db, get_animal_db

router = APIRouter(prefix="/v1/animals", tags=["v1"])


@router.post("/", response_model=AnimalResponseV1, status_code=201)
async def create_animal_v1(
    animal_data: AnimalCreateV1,
    db: AsyncSession = Depends(get_db),
):
    if animal_data.age <= 0:
        raise HTTPException(status_code=400, detail="Age cannot be negative or zero")

    return await create_animal_db(db, animal_data.model_dump())


@router.get("/{animal_id}", response_model=AnimalResponseV1)
async def get_animal_v1(
    animal_id: int,
    db: AsyncSession = Depends(get_db),
):
    animal = await get_animal_db(db, animal_id)

    if not animal:
        raise HTTPException(404, "Not found")

    return animal
