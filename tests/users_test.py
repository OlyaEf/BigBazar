import pytest
from httpx import AsyncClient

from bb.main import app
from bb.users.models import User


@pytest.mark.asyncio
async def test_user_register(test_db):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/users/register",
            json={
                "name": "Test3_Register",
                "email": "test3.reg@example.com",
                "phone": "+71234567893",
                "password": "Reg!Password123!3",
                "confirm_password": "Reg!Password123!3"
               }
            )
        print(response)
        assert response.status_code == 200
        assert response.json()["name"] == "Test3_Register"
        assert response.json()["email"] == "test3.reg@example.com"
        assert response.json()["phone"] == "+71234567893"

        # Очистка данных в конце теста
        await User.all().delete()


@pytest.mark.asyncio
async def test_user_login(test_db):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Сначала регистрируем пользователя
        await client.post("/users/register", json={
            "name": "Test User",
            "email": "test.reg@example.com",
            "phone": "+71234567890",
            "password": "Reg!Password123!",
            "confirm_password": "Reg!Password123!"
        })

        # Затем пытаемся выполнить вход
        response = await client.post(
            "/users/login",
            json={
                "email": "test.reg@example.com",
                "password": "Reg!Password123!",
            }
        )
        print(response)
        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_all_users(test_db, register_and_authenticate_user):
    headers = await register_and_authenticate_user
    async with AsyncClient(app=app, base_url="http://testserver") as client:

        response = await client.get("users/list", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_user_by_id(test_db, registered_user_by_id):
    user_id = await registered_user_by_id  # Получаем ID зарегистрированного пользователя

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id


@pytest.mark.asyncio
async def test_update_user(test_db):
    user_id = 1  # ID пользователя для обновления
    updated_data = {"name": "Updated Name"}
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.patch(f"/users/{user_id}", json=updated_data)
        assert response.status_code == 200
        assert response.json()["name"] == updated_data["name"]


@pytest.mark.asyncio
async def test_delete_user(test_db):
    user_id = 1  # ID пользователя для удаления
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"

