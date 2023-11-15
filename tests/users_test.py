import pytest
from httpx import AsyncClient
from bb.main import app
from bb.users.models import User


# Регистрация пользователя
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
        assert response.status_code == 200
        assert response.json()["name"] == "Test3_Register"
        assert response.json()["email"] == "test3.reg@example.com"
        assert response.json()["phone"] == "+71234567893"
        await User.filter(email="test3.reg@example.com").delete()
        await User.all().delete()


# Аутентификация пользователя
@pytest.mark.asyncio
async def test_user_login(test_db, register_and_authenticate_user):
    user_id, headers = await register_and_authenticate_user
    assert user_id is not None
    assert "Authorization" in headers
    await User.all().delete()


# Получение списка пользователей
@pytest.mark.asyncio
async def test_get_all_users(test_db, register_and_authenticate_user):
    user_id, headers = await register_and_authenticate_user
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/users/list", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        # Очистка данных в конце теста
        await User .all().delete()


# Получение пользователя по ID
@pytest.mark.asyncio
async def test_get_user_by_id(test_db, register_and_authenticate_user):
    user_id, headers = await register_and_authenticate_user
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(f"/users/{user_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["id"] == user_id
        # Очистка данных в конце теста
        await User.filter(id=user_id).delete()


# Обновление пользователя
@pytest.mark.asyncio
async def test_update_user(test_db, register_and_authenticate_user):
    user_id, headers = await register_and_authenticate_user
    updated_data = {"name": "Updated Name"}
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.patch(f"/users/{user_id}", json=updated_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == updated_data["name"]
        # Очистка данных в конце теста
        await User.filter(id=user_id).delete()


# Удаление пользователя
@pytest.mark.asyncio
async def test_delete_user(test_db, register_and_authenticate_user):
    user_id, headers = await register_and_authenticate_user
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.delete(f"/users/{user_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"
        # Очистка данных в конце теста
        await User.filter(id=user_id).delete()