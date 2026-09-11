"""add new table categories and connected with skills
Revision ID: 958e75db63e0
Revises: 5ffb20c403ae
Create Date: 2026-05-03 00:20:11.118967
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "958e75db63e0"
down_revision: Union[str, Sequence[str], None] = "5ffb20c403ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Створюємо таблицю categories
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("icon", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)
    op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=True)
    op.create_index(op.f("ix_categories_slug"), "categories", ["slug"], unique=True)

    # 2. Вставляємо базові категорії
    conn = op.get_bind()
    conn.execute(sa.text("""
        INSERT INTO categories (name, slug, description, icon, is_active)
        VALUES
            ('Програмування', 'programming', 'Мови програмування, фреймворки, алгоритми', 'code', true),
            ('Музика',        'music',       'Гра на інструментах, вокал, теорія музики', 'music', true),
            ('Спорт',         'sports',      'Фізичні вправи, командні та індивідуальні види спорту', 'activity', true),
            ('Мови',          'languages',   'Іноземні мови та переклад', 'globe', true),
            ('Мистецтво',     'art',         'Малювання, скульптура, дизайн', 'pen-tool', true),
            ('Наука',         'science',     'Математика, фізика, хімія, біологія', 'flask', true),
            ('Кулінарія',     'cooking',     'Приготування їжі, рецепти, кулінарні техніки', 'utensils', true),
            ('Інше',          'other',       'Навички, що не вписуються в інші категорії', 'more-horizontal', true)
    """))

    # 3. Дістаємо ID категорії "Інше" як fallback для існуючих рядків
    other_id = conn.execute(
        sa.text("SELECT id FROM categories WHERE slug = 'other'")
    ).scalar()

    # 4. Додаємо колонку як nullable (щоб не впасти на існуючих рядках)
    op.add_column("skills", sa.Column("category_id", sa.Integer(), nullable=True))

    # 5. Заповнюємо існуючі рядки - маппінг зі старого string-поля category
    conn.execute(sa.text("""
        UPDATE skills s
        SET category_id = c.id
        FROM categories c
        WHERE c.slug = s.category
    """))

    # 6. Якщо якийсь рядок не знайшов збіг - ставимо "Інше"
    conn.execute(
        sa.text(f"UPDATE skills SET category_id = {other_id} WHERE category_id IS NULL")
    )

    # 7. Тепер можна зробити NOT NULL
    op.alter_column("skills", "category_id", nullable=False)

    # 8. Прибираємо стару колонку category та її індекс, створюємо новий
    op.drop_index(op.f("ix_skills_category"), table_name="skills")
    op.drop_column("skills", "category")
    op.create_index(
        op.f("ix_skills_category_id"), "skills", ["category_id"], unique=False
    )
    op.create_foreign_key(
        None, "skills", "categories", ["category_id"], ["id"], ondelete="RESTRICT"
    )


def downgrade() -> None:
    op.drop_constraint(None, "skills", type_="foreignkey")
    op.drop_index(op.f("ix_skills_category_id"), table_name="skills")

    # Повертаємо старий string-стовпець
    op.add_column("skills", sa.Column("category", sa.VARCHAR(length=50), nullable=True))

    # Відновлюємо значення зі slug категорії
    conn = op.get_bind()
    conn.execute(sa.text("""
        UPDATE skills s
        SET category = c.slug
        FROM categories c
        WHERE c.id = s.category_id
    """))

    op.alter_column("skills", "category", nullable=False)
    op.drop_column("skills", "category_id")
    op.create_index(op.f("ix_skills_category"), "skills", ["category"], unique=False)

    op.drop_index(op.f("ix_categories_slug"), table_name="categories")
    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
