import pytest

from httpx import AsyncClient

@pytest.mark.parametrize("email,password,status_code", [
    ("kot@kot.com", "kot", 200),
    ("kot@kot.com", "kot", 409),
    ("dog", "dog", 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("sasha@example.com", "sasha", 200),
    ("sasha@example.com", "sasha2", 401),
    ("sasha", "sasha", 422)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code