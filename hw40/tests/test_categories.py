"""
tests/test_categories.py — повна перевірка ендпоінтів /api/categories
"""

import pytest

# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/categories/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_categories_empty(client):
    r = await client.get("/api/categories/")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_categories_returns_active(client, category, inactive_category):
    r = await client.get("/api/categories/")
    assert r.status_code == 200
    data = r.json()
    slugs = [c["slug"] for c in data]
    assert "programming" in slugs
    assert "archive" not in slugs  # inactive не повертається за замовчуванням


@pytest.mark.asyncio
async def test_get_categories_only_active_false(client, category, inactive_category):
    r = await client.get("/api/categories/?only_active=false")
    assert r.status_code == 200
    slugs = [c["slug"] for c in r.json()]
    assert "programming" in slugs
    assert "archive" in slugs


@pytest.mark.asyncio
async def test_get_categories_includes_skills_count(client, category, skill):
    r = await client.get("/api/categories/")
    assert r.status_code == 200
    cat = next(c for c in r.json() if c["slug"] == "programming")
    assert cat["skills_count"] == 1


@pytest.mark.asyncio
async def test_get_categories_pagination(client, category, category2):
    r = await client.get("/api/categories/?limit=1&skip=0")
    assert r.status_code == 200
    assert len(r.json()) == 1


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/categories/{id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_category_by_id(client, category):
    r = await client.get(f"/api/categories/{category.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == category.id
    assert data["slug"] == "programming"
    assert data["is_active"] is True
    assert "skills_count" in data


@pytest.mark.asyncio
async def test_get_category_by_id_not_found(client):
    r = await client.get("/api/categories/99999")
    assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/categories/slug/{slug}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_category_by_slug(client, category):
    r = await client.get("/api/categories/slug/programming")
    assert r.status_code == 200
    assert r.json()["id"] == category.id


@pytest.mark.asyncio
async def test_get_category_by_slug_not_found(client):
    r = await client.get("/api/categories/slug/nonexistent")
    assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/categories/{id}/skills
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_category_skills_empty(client, category):
    r = await client.get(f"/api/categories/{category.id}/skills")
    assert r.status_code == 200
    assert r.json()["skills"] == []


@pytest.mark.asyncio
async def test_get_category_skills_with_data(client, category, skill):
    r = await client.get(f"/api/categories/{category.id}/skills")
    assert r.status_code == 200
    data = r.json()
    assert len(data["skills"]) == 1
    assert data["skills"][0]["title"] == "Python basics"


@pytest.mark.asyncio
async def test_get_category_skills_not_found(client):
    r = await client.get("/api/categories/99999/skills")
    assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
#  POST /api/categories/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_create_category(client):
    payload = {
        "name": "Спорт",
        "slug": "sports",
        "description": "Фізичні вправи",
        "icon": "activity",
    }
    r = await client.post("/api/categories/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Спорт"
    assert data["slug"] == "sports"
    assert data["is_active"] is True
    assert data["skills_count"] == 0
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_category_duplicate_name(client, category):
    r = await client.post(
        "/api/categories/",
        json={
            "name": "Програмування",
            "slug": "programming-2",
        },
    )
    assert r.status_code == 400
    assert "назвою" in r.json()["detail"]


@pytest.mark.asyncio
async def test_create_category_duplicate_slug(client, category):
    r = await client.post(
        "/api/categories/",
        json={
            "name": "Нова категорія",
            "slug": "programming",
        },
    )
    assert r.status_code == 400
    assert "slug" in r.json()["detail"]


@pytest.mark.asyncio
async def test_create_category_invalid_slug(client):
    r = await client.post(
        "/api/categories/",
        json={
            "name": "Тест",
            "slug": "INVALID SLUG!",
        },
    )
    assert r.status_code == 422  # Pydantic validation


@pytest.mark.asyncio
async def test_create_category_minimal(client):
    """Мінімальний payload — лише name та slug."""
    r = await client.post(
        "/api/categories/",
        json={
            "name": "Кулінарія",
            "slug": "cooking",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["description"] is None
    assert data["icon"] is None


# ══════════════════════════════════════════════════════════════════════════════
#  PUT /api/categories/{id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_update_category(client, category):
    r = await client.put(
        f"/api/categories/{category.id}",
        json={
            "description": "Оновлений опис",
            "icon": "terminal",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["description"] == "Оновлений опис"
    assert data["icon"] == "terminal"
    assert data["name"] == "Програмування"  # не змінювалось


@pytest.mark.asyncio
async def test_update_category_deactivate(client, category):
    r = await client.put(f"/api/categories/{category.id}", json={"is_active": False})
    assert r.status_code == 200
    assert r.json()["is_active"] is False


@pytest.mark.asyncio
async def test_update_category_not_found(client):
    r = await client.put("/api/categories/99999", json={"description": "x"})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_update_category_duplicate_name(client, category, category2):
    """Не можна взяти ім'я іншої існуючої категорії."""
    r = await client.put(f"/api/categories/{category.id}", json={"name": "Музика"})
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_update_category_same_name_allowed(client, category):
    """Можна оновити з тим самим ім'ям (сам на себе)."""
    r = await client.put(
        f"/api/categories/{category.id}", json={"name": "Програмування"}
    )
    assert r.status_code == 200


# ══════════════════════════════════════════════════════════════════════════════
#  DELETE /api/categories/{id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_delete_category_empty(client, category):
    r = await client.delete(f"/api/categories/{category.id}")
    assert r.status_code == 204

    # Перевіряємо що справді видалено
    r2 = await client.get(f"/api/categories/{category.id}")
    assert r2.status_code == 404


@pytest.mark.asyncio
async def test_delete_category_with_skills_conflict(client, category, skill):
    """Не можна видалити категорію якщо є навички."""
    r = await client.delete(f"/api/categories/{category.id}")
    assert r.status_code == 409
    assert "навичок" in r.json()["detail"]


@pytest.mark.asyncio
async def test_delete_category_not_found(client):
    r = await client.delete("/api/categories/99999")
    assert r.status_code == 404
