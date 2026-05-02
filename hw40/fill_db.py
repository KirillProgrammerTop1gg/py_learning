import asyncio
from src.database.models import (
    User, Skill, Exchange, Review,
    Category, SkillLevel, ExchangeStatus,
)
from src.database.db import async_session_factory


async def seed_database():
    async with async_session_factory() as db:
        try:
            # --- Categories ---
            categories = [
                Category(
                    name="Програмування",
                    slug="programming",
                    description="Мови програмування, фреймворки, алгоритми",
                    icon="code",
                ),
                Category(
                    name="Музика",
                    slug="music",
                    description="Гра на інструментах, вокал, теорія музики",
                    icon="music",
                ),
                Category(
                    name="Спорт",
                    slug="sports",
                    description="Фізичні вправи, командні та індивідуальні види спорту",
                    icon="activity",
                ),
                Category(
                    name="Мови",
                    slug="languages",
                    description="Іноземні мови та переклад",
                    icon="globe",
                ),
                Category(
                    name="Мистецтво",
                    slug="art",
                    description="Малювання, скульптура, дизайн",
                    icon="pen-tool",
                ),
                Category(
                    name="Наука",
                    slug="science",
                    description="Математика, фізика, хімія, біологія",
                    icon="flask",
                ),
                Category(
                    name="Кулінарія",
                    slug="cooking",
                    description="Приготування їжі, рецепти, кулінарні техніки",
                    icon="utensils",
                ),
                Category(
                    name="Інше",
                    slug="other",
                    description="Навички, що не вписуються в інші категорії",
                    icon="more-horizontal",
                ),
            ]
            db.add_all(categories)
            await db.commit()
            for cat in categories:
                await db.refresh(cat)

            print(f"✅ Додано {len(categories)} категорій")

            # --- Users ---
            users = [
                User(
                    username="alex_dev",
                    email="alex@example.com",
                    full_name="Олександр Петренко",
                    bio="Python розробник, люблю музику",
                ),
                User(
                    username="maria_music",
                    email="maria@example.com",
                    full_name="Марія Коваленко",
                    bio="Викладач музики, хочу вивчити програмування",
                ),
                User(
                    username="ivan_sport",
                    email="ivan@example.com",
                    full_name="Іван Шевченко",
                    bio="Тренер з плавання, цікавлюся технологіями",
                ),
            ]
            db.add_all(users)
            await db.commit()
            for user in users:
                await db.refresh(user)

            print(f"✅ Додано {len(users)} користувачів")

            # --- Skills (з category_id замість category string) ---
            programming_id = categories[0].id  # programming
            music_id       = categories[1].id  # music
            sports_id      = categories[2].id  # sports
            languages_id   = categories[3].id  # languages

            skills = [
                Skill(
                    title="Python програмування",
                    description="Навчу основам Python, Django, FastAPI",
                    category_id=programming_id,
                    level=SkillLevel.advanced,
                    can_teach=True,
                    want_learn=False,
                ),
                Skill(
                    title="Гра на гітарі",
                    description="Можу навчити грати на гітарі з нуля",
                    category_id=music_id,
                    level=SkillLevel.intermediate,
                    can_teach=True,
                    want_learn=False,
                ),
                Skill(
                    title="Плавання",
                    description="Навчу правильній техніці плавання",
                    category_id=sports_id,
                    level=SkillLevel.expert,
                    can_teach=True,
                    want_learn=False,
                ),
                Skill(
                    title="Англійська мова",
                    description="Хочу покращити розмовну англійську",
                    category_id=languages_id,
                    level=SkillLevel.beginner,
                    can_teach=False,
                    want_learn=True,
                ),
            ]
            db.add_all(skills)
            await db.commit()
            for skill in skills:
                await db.refresh(skill)

            print(f"✅ Додано {len(skills)} навичок")

            # --- User ↔ Skill associations ---
            for i in range(min(len(users), len(skills))):
                users[i].skills.append(skills[i])
            await db.commit()

            # --- Exchanges ---
            exchange1 = Exchange(
                sender_id=users[0].id,
                receiver_id=users[1].id,
                skill_id=skills[1].id,
                message="Привіт! Хочу навчитися грати на гітарі, можу навчити Python",
                hours_proposed=5,
                status=ExchangeStatus.completed,
            )
            exchange2 = Exchange(
                sender_id=users[1].id,
                receiver_id=users[0].id,
                skill_id=skills[0].id,
                message="Давай обмінюємося знаннями!",
                hours_proposed=5,
                status=ExchangeStatus.pending,
            )
            db.add_all([exchange1, exchange2])
            await db.commit()
            await db.refresh(exchange1)
            await db.refresh(exchange2)

            print("✅ Додано 2 обміни")

            # --- Reviews ---
            review1 = Review(
                exchange_id=exchange1.id,
                reviewer_id=users[0].id,
                reviewed_id=users[1].id,
                rating=5,
                comment="Чудовий викладач! Дуже терпляче пояснює",
            )
            review2 = Review(
                exchange_id=exchange1.id,
                reviewer_id=users[1].id,
                reviewed_id=users[0].id,
                rating=5,
                comment="Відмінно пояснює програмування, рекомендую!",
            )
            db.add_all([review1, review2])
            await db.commit()

            print("✅ Додано 2 відгуки")
            print("\n🎉 База даних успішно заповнена тестовими даними!")

        except Exception as e:
            await db.rollback()
            print(f"❌ Помилка при заповненні бази даних: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_database())