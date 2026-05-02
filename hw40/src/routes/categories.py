from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryWithSkillsResponse,
)
from src.repository import categories as repository_categories

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
async def read_categories(
    skip: int = Query(0, ge=0, description="Кількість записів, які потрібно пропустити (пагінація)"),
    limit: int = Query(100, ge=1, le=500, description="Максимальна кількість записів у відповіді"),
    only_active: bool = Query(True, description="Якщо true — повертає лише активні категорії"),
    db: AsyncSession = Depends(get_db),
):
    """
    Отримати список усіх категорій навичок.

    Категорії відсортовані за назвою. За замовчуванням повертаються лише активні.
    """
    categories = await repository_categories.get_categories(skip, limit, only_active, db)

    # Додаємо skills_count до кожної категорії
    result = []
    for cat in categories:
        count = await repository_categories.get_skills_count_per_category(cat.id, db)
        response = CategoryResponse.model_validate(cat)
        response.skills_count = count
        result.append(response)

    return result


@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category(
    category_id: int = Path(..., ge=1, description="Унікальний ідентифікатор категорії"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати категорію за ID."""
    category = await repository_categories.get_category(category_id, db)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категорію з ID {category_id} не знайдено",
        )
    count = await repository_categories.get_skills_count_per_category(category_id, db)
    response = CategoryResponse.model_validate(category)
    response.skills_count = count
    return response


@router.get("/slug/{slug}", response_model=CategoryResponse)
async def read_category_by_slug(
    slug: str = Path(..., description="URL-slug категорії (напр. 'programming', 'music')"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати категорію за slug."""
    category = await repository_categories.get_category_by_slug(slug, db)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категорію зі slug '{slug}' не знайдено",
        )
    count = await repository_categories.get_skills_count_per_category(category.id, db)
    response = CategoryResponse.model_validate(category)
    response.skills_count = count
    return response


@router.get("/{category_id}/skills", response_model=CategoryWithSkillsResponse)
async def read_category_skills(
    category_id: int = Path(..., ge=1, description="Унікальний ідентифікатор категорії, чиї навички потрібно отримати"),
    db: AsyncSession = Depends(get_db),
):
    """Отримати категорію разом з усіма її навичками."""
    category = await repository_categories.get_category_with_skills(category_id, db)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категорію з ID {category_id} не знайдено",
        )
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Створити нову категорію навичок.

    - **name**: унікальна назва категорії
    - **slug**: унікальний URL-ідентифікатор (лише малі літери, цифри, дефіс)
    - **description**: необов'язковий опис
    - **icon**: назва іконки для UI (необов'язково)
    """
    if await repository_categories.get_category_by_name(category.name, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категорія з назвою '{category.name}' вже існує",
        )
    if await repository_categories.get_category_by_slug(category.slug, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категорія зі slug '{category.slug}' вже існує",
        )

    db_category = await repository_categories.create_category(category, db)
    response = CategoryResponse.model_validate(db_category)
    response.skills_count = 0
    return response


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int = Path(..., ge=1, description="Унікальний ідентифікатор категорії, яку потрібно оновити"),
    category_update: CategoryUpdate = ...,
    db: AsyncSession = Depends(get_db),
):
    """
    Оновити категорію.

    Можна оновити будь-яке поле, включаючи `is_active` для деактивації категорії.
    """
    # Перевірка унікальності name/slug якщо вони змінюються
    if category_update.name:
        existing = await repository_categories.get_category_by_name(category_update.name, db)
        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Категорія з назвою '{category_update.name}' вже існує",
            )
    if category_update.slug:
        existing = await repository_categories.get_category_by_slug(category_update.slug, db)
        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Категорія зі slug '{category_update.slug}' вже існує",
            )

    db_category = await repository_categories.update_category(category_id, category_update, db)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категорію з ID {category_id} не знайдено",
        )

    count = await repository_categories.get_skills_count_per_category(category_id, db)
    response = CategoryResponse.model_validate(db_category)
    response.skills_count = count
    return response


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., ge=1, description="Унікальний ідентифікатор категорії, яку потрібно видалити"),
    db: AsyncSession = Depends(get_db),
):
    """
    Видалити категорію.

    **Увага:** видалення неможливе якщо до категорії прив'язані навички.
    Спочатку перенесіть або видаліть усі навички цієї категорії.
    """
    try:
        db_category = await repository_categories.delete_category(category_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категорію з ID {category_id} не знайдено",
        )
    return None