import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from bb.core.config import MODELS, POSTGRES_PASSWORD, \
    POSTGRES_HOST, POSTGRES_PORT
from bb.main import app

TEST_DB_URL = f'postgres://postgres:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/db_test_bb'


@pytest.fixture
def event_loop():
    from asyncio import get_event_loop
    loop = get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_db(event_loop):
    async def init():
        await Tortoise.init(
            db_url=TEST_DB_URL,
            modules={'models': [*MODELS]}
        )
        await Tortoise.generate_schemas()

    async def fini():
        await Tortoise.close_connections()

    event_loop.run_until_complete(init())
    yield
    event_loop.run_until_complete(fini())


@pytest.fixture
async def register_and_authenticate_user():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Регистрация пользователя
        await client.post("/users/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+71234567890",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })

        # Аутентификация пользователя
        login_response = await client.post("/users/login", json={
            "email": "test@example.com",
            "password": "Password123!"
        })
        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers


# conftest.py

@pytest.fixture
async def registered_user_by_id():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Регистрация пользователя
        response = await client.post("/users/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+71234567890",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        user_id = response.json()["id"]  # Получение ID пользователя
        return user_id
