from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import SkillCreate, SkillUpdate, SkillResponse, SkillShortResponse
from src.repository import skills as repository_skills

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/", response_model=List[SkillResponse])
async def read_skills(
    skip: int = Query(
        0, ge=0, description="Кількість записів, які потрібно пропустити (пагінація)"
    ),
    limit: int = Query(
        100, ge=1, le=500, description="Максимальна кількість записів у відповіді"
    ),
    category_id: Optional[int] = Query(
        None, ge=1, description="Фільтр за ID категорії навички"
    ),
    can_teach: Optional[bool] = Query(
        None,
        description="Якщо true — повертає лише навички, які користувачі готові викладати",
    ),
    want_learn: Optional[bool] = Query(
        None,
        description="Якщо true — повертає лише навички, які користувачі хочуть вивчити",
    ),
    search: Optional[str] = Query(
        None,
        min_length=1,
        description="Пошук за назвою або описом навички (часткове співпадіння)",
    ),
    db: AsyncSession = Depends(get_db),
):
    """Отримати список навичок з можливістю фільтрації."""
    return await repository_skills.get_skills(
        skip, limit, category_id, can_teach, want_learn, search, db
    )


@router.get("/{skill_id}", response_model=SkillResponse)
async def read_skill(
    skill_id: int = Path(..., ge=1, description="Унікальний ідентифікатор навички"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати детальну інформацію про навичку."""
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
    user_id: int = Query(
        1,
        ge=1,
        description="ID користувача, який створює навичку (тимчасово, поки немає автентифікації)",
    ),
    db: AsyncSession = Depends(get_db),
):
    """Створити нову навичку."""
    try:
        return await repository_skills.create_skill(skill, user_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: int = Path(
        ..., ge=1, description="Унікальний ідентифікатор навички, яку потрібно оновити"
    ),
    skill_update: SkillUpdate = ...,
    db: AsyncSession = Depends(get_db),
):
    """Оновити існуючу навичку."""
    try:
        skill = await repository_skills.update_skill(skill_id, skill_update, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Навичка з ID {skill_id} не знайдена",
        )
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: int = Path(
        ..., ge=1, description="Унікальний ідентифікатор навички, яку потрібно видалити"
    ),
    db: AsyncSession = Depends(get_db),
):
    """Видалити навичку."""
    skill = await repository_skills.delete_skill(skill_id, db)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Навичка з ID {skill_id} не знайдена",
        )
    return None


@router.get("/{skill_id}/matches")
async def find_matches(
    skill_id: int = Path(
        ...,
        ge=1,
        description="Унікальний ідентифікатор навички, для якої шукаються потенційні збіги для обміну",
    ),
    db: AsyncSession = Depends(get_db),
):
    """Знайти потенційні збіги для обміну навичками."""
    matches = await repository_skills.find_skill_matches(skill_id, db)
    if not matches["skill"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Навичка з ID {skill_id} не знайдена",
        )
    return {
        "skill": SkillShortResponse.model_validate(matches["skill"]),
        "matches": [
            SkillShortResponse.model_validate(
                match["skill"] if isinstance(match, dict) else match
            )
            for match in matches["matches"]
        ],
        "matches_count": len(matches["matches"]),
    }
