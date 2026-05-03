"""
tests/test_reviews.py — повна перевірка ендпоінтів /api/reviews
"""

import pytest

# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/reviews/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_reviews_empty(client):
    r = await client.get("/api/reviews/")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_reviews_returns_list(client, review):
    r = await client.get("/api/reviews/")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    rv = data[0]
    assert rv["rating"] == 5
    assert rv["comment"] == "Чудово!"


@pytest.mark.asyncio
async def test_get_reviews_response_fields(client, review):
    r = await client.get("/api/reviews/")
    rv = r.json()[0]
    for field in (
        "id",
        "exchange_id",
        "reviewer_id",
        "reviewed_id",
        "rating",
        "reviewer",
        "reviewed",
    ):
        assert field in rv


@pytest.mark.asyncio
async def test_get_reviews_filter_by_user_id(client, review, user_b):
    r = await client.get(f"/api/reviews/?user_id={user_b.id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["reviewed_id"] == user_b.id


@pytest.mark.asyncio
async def test_get_reviews_filter_by_wrong_user(client, review, user_a):
    """user_a — reviewer, не reviewed. Фільтр по reviewed_id → порожньо."""
    r = await client.get(f"/api/reviews/?user_id={user_a.id}")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_reviews_pagination(client, review):
    r = await client.get("/api/reviews/?limit=1&skip=0")
    assert r.status_code == 200
    assert len(r.json()) == 1

    r2 = await client.get("/api/reviews/?limit=10&skip=1")
    assert r2.status_code == 200
    assert r2.json() == []


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/reviews/{review_id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_review_by_id(client, review):
    r = await client.get(f"/api/reviews/{review.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == review.id
    assert data["rating"] == 5


@pytest.mark.asyncio
async def test_get_review_not_found(client):
    r = await client.get("/api/reviews/99999")
    assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
#  POST /api/reviews/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_create_review(client, exchange_completed, user_a, user_b):
    r = await client.post(
        f"/api/reviews/?reviewer_id={user_a.id}",
        json={
            "exchange_id": exchange_completed.id,
            "rating": 4,
            "comment": "Непогано!",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["rating"] == 4
    assert data["reviewer_id"] == user_a.id
    assert data["reviewed_id"] == user_b.id
    assert data["comment"] == "Непогано!"


@pytest.mark.asyncio
async def test_create_review_other_side(client, exchange_completed, user_a, user_b):
    """Обидва учасники можуть залишити відгук."""
    r = await client.post(
        f"/api/reviews/?reviewer_id={user_b.id}",
        json={
            "exchange_id": exchange_completed.id,
            "rating": 5,
            "comment": "Відмінно!",
        },
    )
    assert r.status_code == 201
    assert r.json()["reviewer_id"] == user_b.id
    assert r.json()["reviewed_id"] == user_a.id


@pytest.mark.asyncio
async def test_create_review_on_pending_exchange_fails(
    client, exchange_pending, user_a
):
    """Не можна залишити відгук на незавершений обмін."""
    r = await client.post(
        f"/api/reviews/?reviewer_id={user_a.id}",
        json={
            "exchange_id": exchange_pending.id,
            "rating": 5,
        },
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_create_review_non_participant_fails(
    client, exchange_completed, db_session
):
    """Третій юзер не може залишити відгук на чужий обмін."""
    from src.database.models import User

    outsider = User(username="outsider", email="out@test.com")
    db_session.add(outsider)
    await db_session.commit()

    r = await client.post(
        f"/api/reviews/?reviewer_id={outsider.id}",
        json={
            "exchange_id": exchange_completed.id,
            "rating": 3,
        },
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_create_review_duplicate_fails(client, exchange_completed, user_a):
    """Один учасник не може залишити два відгуки на один обмін."""
    payload = {"exchange_id": exchange_completed.id, "rating": 5}

    r1 = await client.post(f"/api/reviews/?reviewer_id={user_a.id}", json=payload)
    assert r1.status_code == 201

    r2 = await client.post(f"/api/reviews/?reviewer_id={user_a.id}", json=payload)
    assert r2.status_code == 400


@pytest.mark.asyncio
async def test_create_review_rating_out_of_range(client, exchange_completed, user_a):
    r = await client.post(
        f"/api/reviews/?reviewer_id={user_a.id}",
        json={"exchange_id": exchange_completed.id, "rating": 6},  # max=5
    )
    assert r.status_code == 422

    r2 = await client.post(
        f"/api/reviews/?reviewer_id={user_a.id}",
        json={"exchange_id": exchange_completed.id, "rating": 0},  # min=1
    )
    assert r2.status_code == 422


@pytest.mark.asyncio
async def test_create_review_nonexistent_exchange(client, user_a):
    r = await client.post(
        f"/api/reviews/?reviewer_id={user_a.id}",
        json={"exchange_id": 99999, "rating": 5},
    )
    assert r.status_code == 400


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/reviews/user/{user_id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_user_reviews(client, review, user_b):
    r = await client.get(f"/api/reviews/user/{user_b.id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["reviewed_id"] == user_b.id


@pytest.mark.asyncio
async def test_get_user_reviews_empty(client, user_a):
    r = await client.get(f"/api/reviews/user/{user_a.id}")
    assert r.status_code == 200
    assert r.json() == []


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/reviews/user/{user_id}/rating
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_user_rating(client, review, user_b):
    r = await client.get(f"/api/reviews/user/{user_b.id}/rating")
    assert r.status_code == 200
    data = r.json()
    assert data["user_id"] == user_b.id
    assert data["average_rating"] == 5.0
    assert data["total_reviews"] == 1


@pytest.mark.asyncio
async def test_get_user_rating_no_reviews(client, user_a):
    """Без відгуків — повертає нулі, а не 404."""
    r = await client.get(f"/api/reviews/user/{user_a.id}/rating")
    assert r.status_code == 200
    data = r.json()
    assert data["average_rating"] == 0
    assert data["total_reviews"] == 0


@pytest.mark.asyncio
async def test_get_user_rating_average(
    client, exchange_completed, user_a, user_b, db_session
):
    """Перевіряємо що середнє рахується правильно."""
    from src.database.models import Review, Exchange, ExchangeStatus, Skill, SkillLevel
    from tests.conftest import category  # type: ignore

    # Додаємо другий відгук з рейтингом 3
    r2 = Review(
        exchange_id=exchange_completed.id,
        reviewer_id=user_b.id,
        reviewed_id=user_a.id,
        rating=3,
        comment="Непогано",
    )
    db_session.add(r2)
    await db_session.commit()

    r = await client.get(f"/api/reviews/user/{user_a.id}/rating")
    assert r.status_code == 200
    data = r.json()
    assert data["total_reviews"] == 1  # тільки відгуки де user_a є reviewed
    assert data["average_rating"] == 3.0
