"""
tests/test_root.py — перевірка кореневих ендпоінтів застосунку
"""

import pytest


@pytest.mark.asyncio
async def test_root(client):
    r = await client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "message" in data
    assert "endpoints" in data
    assert "categories" in data["endpoints"]
    assert "users" in data["endpoints"]
    assert "skills" in data["endpoints"]
    assert "exchanges" in data["endpoints"]
    assert "reviews" in data["endpoints"]


@pytest.mark.asyncio
async def test_health_check(client):
    r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_docs_available(client):
    r = await client.get("/docs")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_redoc_available(client):
    r = await client.get("/redoc")
    assert r.status_code == 200
