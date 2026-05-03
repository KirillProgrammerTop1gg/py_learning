"""
tests/test_stats.py — повна перевірка ендпоінтів /api/stats
"""

import pytest

# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/stats/top-skills
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_top_skills_empty(client):
    r = await client.get("/api/stats/top-skills")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_top_skills_returns_list(client, skill, skill2):
    r = await client.get("/api/stats/top-skills")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_top_skills_response_fields(client, skill):
    r = await client.get("/api/stats/top-skills")
    assert r.status_code == 200
    item = r.json()[0]
    for field in ("rank", "skill_id", "title", "users_count"):
        assert field in item


@pytest.mark.asyncio
async def test_top_skills_rank_order(client, skill, skill2, user_a, user_b, db_session):
    """skill прив'язаний до user_a (1 юзер), skill2 — до нікого (0).
    Після додавання user_b до skill → skill матиме 2 юзери і буде першим."""
    user_a.skills.append(skill2)  # тепер skill2 теж має 1 юзера
    user_b.skills.append(skill)  # skill → 2 юзери
    await db_session.commit()

    r = await client.get("/api/stats/top-skills?limit=2")
    assert r.status_code == 200
    data = r.json()
    assert data[0]["rank"] == 1
    assert data[0]["users_count"] >= data[1]["users_count"]


@pytest.mark.asyncio
async def test_top_skills_limit(client, skill, skill2):
    r = await client.get("/api/stats/top-skills?limit=1")
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.asyncio
async def test_top_skills_limit_validation(client):
    r = await client.get("/api/stats/top-skills?limit=0")
    assert r.status_code == 422

    r2 = await client.get("/api/stats/top-skills?limit=101")
    assert r2.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/stats/active-users
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_active_users_empty(client):
    r = await client.get("/api/stats/active-users")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_active_users_returns_list(client, user_a, user_b):
    r = await client.get("/api/stats/active-users")
    assert r.status_code == 200
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_active_users_response_fields(client, user_a):
    r = await client.get("/api/stats/active-users")
    assert r.status_code == 200
    u = r.json()[0]
    for field in (
        "rank",
        "user_id",
        "username",
        "sent_exchanges",
        "received_exchanges",
        "total_exchanges",
        "reviews_given",
        "skills_count",
        "activity_score",
    ):
        assert field in u


@pytest.mark.asyncio
async def test_active_users_activity_score(
    client, user_a, user_b, exchange_pending, review
):
    """user_a надіслав 1 обмін + 1 відгук = activity_score >= 2."""
    r = await client.get("/api/stats/active-users")
    assert r.status_code == 200
    data = r.json()

    alice = next(u for u in data if u["username"] == "alice")
    assert alice["sent_exchanges"] >= 1
    assert alice["reviews_given"] >= 1
    assert alice["activity_score"] >= 2


@pytest.mark.asyncio
async def test_active_users_sorted_by_score(
    client, user_a, user_b, exchange_pending, exchange_completed
):
    """Перший юзер повинен мати activity_score >= другого."""
    r = await client.get("/api/stats/active-users")
    assert r.status_code == 200
    data = r.json()
    if len(data) >= 2:
        assert data[0]["activity_score"] >= data[1]["activity_score"]


@pytest.mark.asyncio
async def test_active_users_limit(client, user_a, user_b):
    r = await client.get("/api/stats/active-users?limit=1")
    assert r.status_code == 200
    assert len(r.json()) == 1


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/stats/exchange-success-rate
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_exchange_success_rate_empty(client):
    r = await client.get("/api/stats/exchange-success-rate")
    assert r.status_code == 200
    data = r.json()
    assert data["total_exchanges"] == 0
    assert data["success_rate_percent"] == 0.0
    assert data["failure_rate_percent"] == 0.0


@pytest.mark.asyncio
async def test_exchange_success_rate_response_fields(client):
    r = await client.get("/api/stats/exchange-success-rate")
    assert r.status_code == 200
    data = r.json()
    assert "total_exchanges" in data
    assert "success_rate_percent" in data
    assert "failure_rate_percent" in data
    assert "breakdown" in data
    breakdown = data["breakdown"]
    for key in ("completed", "pending", "accepted", "rejected", "cancelled"):
        assert key in breakdown


@pytest.mark.asyncio
async def test_exchange_success_rate_with_data(
    client, exchange_pending, exchange_completed
):
    r = await client.get("/api/stats/exchange-success-rate")
    assert r.status_code == 200
    data = r.json()

    assert data["total_exchanges"] == 2
    assert data["breakdown"]["completed"] == 1
    assert data["breakdown"]["pending"] == 1
    assert data["success_rate_percent"] == 50.0
    assert data["failure_rate_percent"] == 0.0


@pytest.mark.asyncio
async def test_exchange_success_rate_all_completed(client, exchange_completed):
    r = await client.get("/api/stats/exchange-success-rate")
    assert r.status_code == 200
    data = r.json()
    assert data["success_rate_percent"] == 100.0


@pytest.mark.asyncio
async def test_exchange_success_rate_calculation(
    client, db_session, user_a, user_b, skill
):
    """2 rejected з 4 = 50% failure_rate."""
    from src.database.models import Exchange, ExchangeStatus

    for status in [
        ExchangeStatus.completed,
        ExchangeStatus.rejected,
        ExchangeStatus.rejected,
        ExchangeStatus.cancelled,
    ]:
        ex = Exchange(
            sender_id=user_a.id,
            receiver_id=user_b.id,
            skill_id=skill.id,
            hours_proposed=1,
            status=status,
        )
        db_session.add(ex)
    await db_session.commit()

    r = await client.get("/api/stats/exchange-success-rate")
    assert r.status_code == 200
    data = r.json()
    assert data["total_exchanges"] == 4
    assert data["breakdown"]["completed"] == 1
    assert data["breakdown"]["rejected"] == 2
    assert data["breakdown"]["cancelled"] == 1
    # (2 rejected + 1 cancelled) / 4 * 100 = 75%
    assert data["failure_rate_percent"] == 75.0
    assert data["success_rate_percent"] == 25.0
