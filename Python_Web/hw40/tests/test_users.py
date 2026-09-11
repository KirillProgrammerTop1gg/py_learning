"""
tests/test_users.py — повна перевірка ендпоінтів /api/users
"""

import pytest

# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/users/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_users_empty(client):
    r = await client.get("/api/users/")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_users_returns_list(client, user_a, user_b):
    r = await client.get("/api/users/")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    usernames = {u["username"] for u in data}
    assert {"alice", "bob"} == usernames


@pytest.mark.asyncio
async def test_get_users_pagination_skip(client, user_a, user_b):
    r = await client.get("/api/users/?skip=1&limit=10")
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.asyncio
async def test_get_users_pagination_limit(client, user_a, user_b):
    r = await client.get("/api/users/?limit=1")
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.asyncio
async def test_get_users_response_fields(client, user_a):
    r = await client.get("/api/users/")
    assert r.status_code == 200
    u = r.json()[0]
    for field in ("id", "username", "email", "full_name"):
        assert field in u


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/users/{user_id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_user_by_id(client, user_a):
    r = await client.get(f"/api/users/{user_a.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == user_a.id
    assert data["username"] == "alice"
    assert data["email"] == "alice@test.com"


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    r = await client.get("/api/users/99999")
    assert r.status_code == 404
    assert "не знайдено" in r.json()["detail"]


# ══════════════════════════════════════════════════════════════════════════════
#  POST /api/users/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_create_user(client):
    payload = {
        "username": "charlie",
        "email": "charlie@test.com",
        "full_name": "Charlie C",
        "bio": "Новий юзер",
        "location": "Kyiv",
    }
    r = await client.post("/api/users/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == "charlie"
    assert data["email"] == "charlie@test.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_user_minimal(client):
    """Лише обов'язкові поля."""
    r = await client.post(
        "/api/users/",
        json={
            "username": "minimal",
            "email": "minimal@test.com",
        },
    )
    assert r.status_code == 201
    assert r.json()["full_name"] is None


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client, user_a):
    r = await client.post(
        "/api/users/",
        json={
            "username": "new_user",
            "email": "alice@test.com",  # вже існує
        },
    )
    assert r.status_code == 400
    assert "Email" in r.json()["detail"]


@pytest.mark.asyncio
async def test_create_user_duplicate_username(client, user_a):
    r = await client.post(
        "/api/users/",
        json={
            "username": "alice",  # вже існує
            "email": "new@test.com",
        },
    )
    assert r.status_code == 400
    assert "Username" in r.json()["detail"]


@pytest.mark.asyncio
async def test_create_user_invalid_email(client):
    r = await client.post(
        "/api/users/",
        json={
            "username": "testuser",
            "email": "not-an-email",
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_create_user_short_username(client):
    r = await client.post(
        "/api/users/",
        json={
            "username": "ab",  # min_length=3
            "email": "x@test.com",
        },
    )
    assert r.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
#  PUT /api/users/{user_id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_update_user(client, user_a):
    r = await client.put(
        f"/api/users/{user_a.id}",
        json={
            "full_name": "Alice Updated",
            "bio": "Нова біографія",
            "location": "Odesa",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["full_name"] == "Alice Updated"
    assert data["bio"] == "Нова біографія"
    assert data["location"] == "Odesa"
    assert data["username"] == "alice"  # не змінювалось


@pytest.mark.asyncio
async def test_update_user_partial(client, user_a):
    """Часткове оновлення — лише одне поле."""
    r = await client.put(f"/api/users/{user_a.id}", json={"bio": "Тільки біо"})
    assert r.status_code == 200
    assert r.json()["bio"] == "Тільки біо"


@pytest.mark.asyncio
async def test_update_user_not_found(client):
    r = await client.put("/api/users/99999", json={"bio": "x"})
    assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/users/{user_id}/skills
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_user_skills_empty(client, user_b):
    r = await client.get(f"/api/users/{user_b.id}/skills")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_user_skills_with_data(client, user_a, skill):
    r = await client.get(f"/api/users/{user_a.id}/skills")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["title"] == "Python basics"


@pytest.mark.asyncio
async def test_get_user_skills_not_found(client):
    r = await client.get("/api/users/99999/skills")
    assert r.status_code == 404
