from pydantic import BaseModel, ConfigDict, Field
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Dish, get_db


app = FastAPI()


# Схема для ВХІДНИХ даних (те, що користувач надсилає)
class DishCreate(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)  # gt=0 означає Greater Than 0
    description: str | None = None


# Схема для ВИХІДНИХ даних (те, що ми віддаємо клієнту)
class DishResponse(BaseModel):
    id: int
    name: str
    price: float

    # ЦЯ НАЛАШТУВАННЯ МАГІЧНЕ.
    # Вона вчить Pydantic читати дані не з JSON-словника, а з атрибутів ORM-моделі (dish.name)
    model_config = ConfigDict(from_attributes=True)


# Оновлений безпечний маршрут
@app.post("/safe-dishes", response_model=DishResponse)
async def safe_create(dish_in: DishCreate, db: AsyncSession = Depends(get_db)):
    # Перетворюємо валідовану Pydantic-модель на словник і розпаковуємо в ORM
    new_dish = Dish(**dish_in.model_dump())
    db.add(new_dish)
    await db.commit()
    await db.refresh(new_dish)

    # FastAPI сам побачить response_model=DishResponse,
    # візьме new_dish і пропустить його через ConfigDict(from_attributes=True)
    return new_dish


@app.get("/dishes")
async def get_all_dishes(db: AsyncSession = Depends(get_db)):
    # 1. Будуємо SQL-запит (ще не йдемо в базу!)
    # Еквівалент: SELECT * FROM dishes ORDER BY price ASC
    stmt = select(Dish).order_by(Dish.price)

    # 2. Йдемо в базу. await блокує поточну функцію, звільняючи Event Loop
    result = await db.execute(stmt)

    # 3. Розпаковуємо результат.
    # db.execute повертає кортежі (tuples). scalars() бере перший елемент кожного кортежу,
    # перетворюючи сирі рядки таблиці на красиві об'єкти класу Dish.
    dishes = result.scalars().all()

    return dishes


@app.post("/dishes")
async def create_dish(name: str, price: float, db: AsyncSession = Depends(get_db)):
    # Створюємо об'єкт у пам'яті Python
    new_dish = Dish(name=name, price=price)

    # Додаємо в робочий зошит сесії
    db.add(new_dish)

    # Зберігаємо в БД (тут генерується SQL INSERT)
    await db.commit()

    # Оскільки БД генерує ID автоматично, наш new_dish поки що не знає свого ID.
    # refresh затягує свіжі дані з БД назад в об'єкт.
    await db.refresh(new_dish)

    return new_dish