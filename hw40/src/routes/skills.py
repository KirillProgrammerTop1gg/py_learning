from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.db import get_db
from src.schemas import SkillCreate, SkillUpdate, SkillResponse
from src.repository import skills as repository_skills

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/", response_model=List[SkillResponse])
async def read_skills(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    can_teach: Optional[bool] = None,
    want_learn: Optional[bool] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Отримати список навичок з можливістю фільтрації.

    - **skip**: кількість записів, які потрібно пропустити
    - **limit**: максимальна кількість записів у відповіді
    - **category**: фільтр за категорією навички
    - **can_teach**: якщо true, повертає лише навички тих, хто може навчати
    - **want_learn**: якщо true, повертає лише навички тих, хто хоче вчитися
    - **search**: пошуковий рядок для фільтрації за назвою або описом
    """
    return await repository_skills.get_skills(
        skip, limit, category, can_teach, want_learn, search, db
    )


@router.get("/{skill_id}", response_model=SkillResponse)
async def read_skill(skill_id: int, db: AsyncSession = Depends(get_db)):
    """
    Отримати детальну інформацію про навичку.

    - **skill_id**: унікальний ідентифікатор навички
    """
    skill = await repository_skills.get_skill(skill_id, db)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Навичка з ID {skill_id} не знайдена",
        )
    return skill


@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill: SkillCreate,
    user_id: int = 1,  # Тимчасово, поки немає автентифікації
    db: AsyncSession = Depends(get_db),
):
    """
    Створити нову навичку.

    - **skill**: дані нової навички (назва, опис, категорія тощо)
    - **user_id**: ідентифікатор користувача, який створює навичку
    """
    return await repository_skills.create_skill(skill, user_id, db)


@router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: int, skill_update: SkillUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Оновити існуючу навичку.

    - **skill_id**: унікальний ідентифікатор навички
    - **skill_update**: поля навички, які потрібно оновити
    """
    skill = await repository_skills.update_skill(skill_id, skill_update, db)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Навичка з ID {skill_id} не знайдена",
        )
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: int, db: AsyncSession = Depends(get_db)):
    """
    Видалити навичку.

    - **skill_id**: унікальний ідентифікатор навички, яку потрібно видалити
    """
    skill = await repository_skills.delete_skill(skill_id, db)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Навичка з ID {skill_id} не знайдена",
        )
    return None


@router.get("/{skill_id}/matches")
async def find_matches(skill_id: int, db: AsyncSession = Depends(get_db)):
    """
    Знайти потенційні збіги для обміну навичками.

    - **skill_id**: унікальний ідентифікатор навички, для якої шукаються збіги
    """
    matches = await repository_skills.find_skill_matches(skill_id, db)
    if not matches["skill"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Навичка з ID {skill_id} не знайдена",
        )
    return matches
