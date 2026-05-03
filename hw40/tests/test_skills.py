"""
tests/test_skills.py — повна перевірка ендпоінтів /api/skills
"""

import pytest

# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/skills/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_skills_empty(client):
    r = await client.get("/api/skills/")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_skills_returns_list(client, skill, skill2):
    r = await client.get("/api/skills/")
    assert r.status_code == 200
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_get_skills_filter_by_category_id(client, skill, skill2, category):
    r = await client.get(f"/api/skills/?category_id={category.id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["title"] == "Python basics"


@pytest.mark.asyncio
async def test_get_skills_filter_can_teach(client, skill, skill2):
    r = await client.get("/api/skills/?can_teach=true")
    assert r.status_code == 200
    assert all(s["can_teach"] for s in r.json())


@pytest.mark.asyncio
async def test_get_skills_filter_want_learn(client, skill, db_session, category):
    from src.database.models import Skill, SkillLevel

    learner = Skill(
        title="Хочу вивчити Django",
        description="Шукаю репетитора з Django",
        category_id=category.id,
        level=SkillLevel.beginner,
        can_teach=False,
        want_learn=True,
    )
    db_session.add(learner)
    await db_session.commit()

    r = await client.get("/api/skills/?want_learn=true")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["want_learn"] is True


@pytest.mark.asyncio
async def test_get_skills_search(client, skill, skill2):
    r = await client.get("/api/skills/?search=Python")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert "Python" in data[0]["title"]


@pytest.mark.asyncio
async def test_get_skills_search_no_results(client, skill):
    r = await client.get("/api/skills/?search=NONEXISTENT_XYZ")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_skills_pagination(client, skill, skill2):
    r = await client.get("/api/skills/?limit=1&skip=0")
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.asyncio
async def test_get_skills_response_has_category(client, skill):
    r = await client.get("/api/skills/")
    assert r.status_code == 200
    s = r.json()[0]
    assert "category_id" in s
    assert "category" in s
    assert s["category"]["slug"] == "programming"


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/skills/{skill_id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_skill_by_id(client, skill):
    r = await client.get(f"/api/skills/{skill.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == skill.id
    assert data["title"] == "Python basics"
    assert data["can_teach"] is True
    assert isinstance(data["users"], list)


@pytest.mark.asyncio
async def test_get_skill_not_found(client):
    r = await client.get("/api/skills/99999")
    assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
#  POST /api/skills/
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_create_skill(client, category, user_a):
    payload = {
        "title": "FastAPI розробка",
        "description": "Навчу будувати REST API на FastAPI",
        "category_id": category.id,
        "level": "intermediate",
        "can_teach": True,
        "want_learn": False,
    }
    r = await client.post(f"/api/skills/?user_id={user_a.id}", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "FastAPI розробка"
    assert data["category_id"] == category.id
    assert data["can_teach"] is True
    assert "id" in data


@pytest.mark.asyncio
async def test_create_skill_invalid_category(client, user_a):
    r = await client.post(
        f"/api/skills/?user_id={user_a.id}",
        json={
            "title": "Якась навичка",
            "description": "Опис навички не менше 10 символів",
            "category_id": 99999,
            "level": "beginner",
            "can_teach": True,
            "want_learn": False,
        },
    )
    assert r.status_code == 400
    assert "Категорія" in r.json()["detail"]


@pytest.mark.asyncio
async def test_create_skill_inactive_category(client, inactive_category, user_a):
    r = await client.post(
        f"/api/skills/?user_id={user_a.id}",
        json={
            "title": "Якась навичка",
            "description": "Опис навички не менше 10 символів",
            "category_id": inactive_category.id,
            "level": "beginner",
            "can_teach": True,
            "want_learn": False,
        },
    )
    assert r.status_code == 400
    assert "неактивна" in r.json()["detail"]


@pytest.mark.asyncio
async def test_create_skill_both_teach_and_learn_fails(client, category, user_a):
    """can_teach і want_learn одночасно — 422."""
    r = await client.post(
        f"/api/skills/?user_id={user_a.id}",
        json={
            "title": "Конфліктна навичка",
            "description": "Опис навички довший за 10 символів",
            "category_id": category.id,
            "level": "beginner",
            "can_teach": True,
            "want_learn": True,
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_create_skill_short_description(client, category, user_a):
    r = await client.post(
        f"/api/skills/?user_id={user_a.id}",
        json={
            "title": "Тест",
            "description": "Коротко",  # < 10 символів
            "category_id": category.id,
            "level": "beginner",
            "can_teach": True,
            "want_learn": False,
        },
    )
    assert r.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
#  PUT /api/skills/{skill_id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_update_skill(client, skill, category2):
    r = await client.put(
        f"/api/skills/{skill.id}",
        json={
            "title": "Python Advanced",
            "level": "advanced",
            "category_id": category2.id,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Python Advanced"
    assert data["level"] == "advanced"
    assert data["category_id"] == category2.id


@pytest.mark.asyncio
async def test_update_skill_not_found(client):
    r = await client.put("/api/skills/99999", json={"title": "x" * 5})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_update_skill_invalid_category(client, skill):
    r = await client.put(f"/api/skills/{skill.id}", json={"category_id": 99999})
    assert r.status_code == 400


# ══════════════════════════════════════════════════════════════════════════════
#  DELETE /api/skills/{skill_id}
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_delete_skill(client, skill):
    r = await client.delete(f"/api/skills/{skill.id}")
    assert r.status_code == 204

    r2 = await client.get(f"/api/skills/{skill.id}")
    assert r2.status_code == 404


@pytest.mark.asyncio
async def test_delete_skill_not_found(client):
    r = await client.delete("/api/skills/99999")
    assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
#  GET /api/skills/{skill_id}/matches
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_find_matches_no_matches(client, skill):
    r = await client.get(f"/api/skills/{skill.id}/matches")
    assert r.status_code == 200
    data = r.json()
    assert "matches_count" in data
    assert data["matches_count"] == 0
    assert isinstance(data["matches"], list)


@pytest.mark.asyncio
async def test_find_matches_not_found(client):
    r = await client.get("/api/skills/99999/matches")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_find_matches_found(client, db_session, category, skill):
    """skill хоче вчитися — шукаємо того хто може вчити в тій самій категорії."""
    from src.database.models import Skill, SkillLevel

    # Перетворюємо skill на want_learn
    skill.can_teach = False
    skill.want_learn = True
    await db_session.commit()

    teacher = Skill(
        title="Python basics",  # той самий title для ilike-матча
        description="Навчу Python від нуля до джуна",
        category_id=category.id,
        level=SkillLevel.advanced,
        can_teach=True,
        want_learn=False,
    )
    db_session.add(teacher)
    await db_session.commit()

    r = await client.get(f"/api/skills/{skill.id}/matches")
    assert r.status_code == 200
    assert r.json()["matches_count"] >= 1
