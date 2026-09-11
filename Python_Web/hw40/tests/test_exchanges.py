"""
tests/test_exchanges.py — повна перевірка ендпоінтів /api/exchanges
"""

import pytest

# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/exchanges/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_exchanges_empty(client):
    r = await client.get("/api/exchanges/")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_exchanges_returns_list(client, exchange_pending):
    r = await client.get("/api/exchanges/")
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.asyncio
async def test_get_exchanges_response_fields(client, exchange_pending):
    r = await client.get("/api/exchanges/")
    assert r.status_code == 200
    ex = r.json()[0]
    for field in (
        "id",
        "sender_id",
        "receiver_id",
        "skill_id",
        "status",
        "sender",
        "receiver",
        "skill",
    ):
        assert field in ex


@pytest.mark.asyncio
async def test_get_exchanges_filter_by_status(
    client, exchange_pending, exchange_completed
):
    r = await client.get("/api/exchanges/?status_filter=pending")
    assert r.status_code == 200
    data = r.json()
    assert all(e["status"] == "pending" for e in data)
    assert len(data) == 1


@pytest.mark.asyncio
async def test_get_exchanges_filter_by_user_id(
    client, exchange_pending, user_a, user_b
):
    r = await client.get(f"/api/exchanges/?user_id={user_a.id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    ex = data[0]
    assert ex["sender_id"] == user_a.id or ex["receiver_id"] == user_a.id


@pytest.mark.asyncio
async def test_get_exchanges_sort_asc(client, exchange_pending, exchange_completed):
    r = await client.get("/api/exchanges/?sort_order=asc")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    # Перший створений — менший id
    assert data[0]["id"] < data[1]["id"]


@pytest.mark.asyncio
async def test_get_exchanges_sort_desc(client, exchange_pending, exchange_completed):
    r = await client.get("/api/exchanges/?sort_order=desc")
    assert r.status_code == 200
    data = r.json()
    assert data[0]["id"] > data[1]["id"]


@pytest.mark.asyncio
async def test_get_exchanges_invalid_sort(client):
    r = await client.get("/api/exchanges/?sort_order=invalid")
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_get_exchanges_date_filter_invalid_range(client):
    r = await client.get(
        "/api/exchanges/?from_date=2025-12-31T00:00:00&to_date=2025-01-01T00:00:00"
    )
    assert r.status_code == 400
    assert "from_date" in r.json()["detail"]


@pytest.mark.asyncio
async def test_get_exchanges_pagination(client, exchange_pending, exchange_completed):
    r = await client.get("/api/exchanges/?limit=1")
    assert r.status_code == 200
    assert len(r.json()) == 1


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/exchanges/my/sent  &  /api/exchanges/my/received
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_my_sent(client, exchange_pending, user_a):
    r = await client.get(f"/api/exchanges/my/sent?user_id={user_a.id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["sender_id"] == user_a.id


@pytest.mark.asyncio
async def test_get_my_received(client, exchange_pending, user_b):
    r = await client.get(f"/api/exchanges/my/received?user_id={user_b.id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["receiver_id"] == user_b.id


@pytest.mark.asyncio
async def test_get_my_sent_empty(client, user_b):
    r = await client.get(f"/api/exchanges/my/sent?user_id={user_b.id}")
    assert r.status_code == 200
    assert r.json() == []


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/exchanges/{exchange_id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_exchange_by_id(client, exchange_pending):
    r = await client.get(f"/api/exchanges/{exchange_pending.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == exchange_pending.id
    assert data["status"] == "pending"
    assert data["hours_proposed"] == 3
    assert data["message"] == "Давай обміняємось!"


@pytest.mark.asyncio
async def test_get_exchange_not_found(client):
    r = await client.get("/api/exchanges/99999")
    assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
#  POST /api/exchanges/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_create_exchange(client, user_a, user_b, skill):
    r = await client.post(
        f"/api/exchanges/?sender_id={user_a.id}",
        json={
            "receiver_id": user_b.id,
            "skill_id": skill.id,
            "message": "Хочу обмінятись навичками",
            "hours_proposed": 4,
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["sender_id"] == user_a.id
    assert data["receiver_id"] == user_b.id
    assert data["status"] == "pending"
    assert data["hours_proposed"] == 4


@pytest.mark.asyncio
async def test_create_exchange_self(client, user_a, skill):
    """Не можна створити обмін з самим собою."""
    r = await client.post(
        f"/api/exchanges/?sender_id={user_a.id}",
        json={
            "receiver_id": user_a.id,
            "skill_id": skill.id,
            "hours_proposed": 1,
        },
    )
    assert r.status_code == 400
    assert "самим собою" in r.json()["detail"]


@pytest.mark.asyncio
async def test_create_exchange_invalid_skill(client, user_a, user_b):
    r = await client.post(
        f"/api/exchanges/?sender_id={user_a.id}",
        json={
            "receiver_id": user_b.id,
            "skill_id": 99999,
            "hours_proposed": 1,
        },
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_create_exchange_hours_out_of_range(client, user_a, user_b, skill):
    r = await client.post(
        f"/api/exchanges/?sender_id={user_a.id}",
        json={
            "receiver_id": user_b.id,
            "skill_id": skill.id,
            "hours_proposed": 11,  # max=10
        },
    )
    assert r.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
#  PUT /api/exchanges/{exchange_id}  — зміна статусу
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_accept_exchange_by_receiver(client, exchange_pending, user_b):
    r = await client.put(
        f"/api/exchanges/{exchange_pending.id}?current_user_id={user_b.id}",
        json={"status": "accepted"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "accepted"


@pytest.mark.asyncio
async def test_reject_exchange_by_receiver(client, exchange_pending, user_b):
    r = await client.put(
        f"/api/exchanges/{exchange_pending.id}?current_user_id={user_b.id}",
        json={"status": "rejected"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "rejected"


@pytest.mark.asyncio
async def test_accept_exchange_by_sender_forbidden(client, exchange_pending, user_a):
    """Відправник не може прийняти власний запит."""
    r = await client.put(
        f"/api/exchanges/{exchange_pending.id}?current_user_id={user_a.id}",
        json={"status": "accepted"},
    )
    assert r.status_code == 404  # repository повертає None → 404


@pytest.mark.asyncio
async def test_cancel_exchange_by_sender(client, exchange_pending, user_a):
    r = await client.put(
        f"/api/exchanges/{exchange_pending.id}?current_user_id={user_a.id}",
        json={"status": "cancelled"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancel_exchange_by_receiver(client, exchange_pending, user_b):
    r = await client.put(
        f"/api/exchanges/{exchange_pending.id}?current_user_id={user_b.id}",
        json={"status": "cancelled"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_update_exchange_not_found(client, user_a):
    r = await client.put(
        f"/api/exchanges/99999?current_user_id={user_a.id}",
        json={"status": "accepted"},
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_update_exchange_with_message(client, exchange_pending, user_b):
    r = await client.put(
        f"/api/exchanges/{exchange_pending.id}?current_user_id={user_b.id}",
        json={"status": "accepted", "message": "Чудово, домовились!"},
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Чудово, домовились!"
