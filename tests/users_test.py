import pytest
from httpx import AsyncClient

from bb.main import app


@pytest.mark.asyncio
async def test_user_register(test_db):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/users/register",
            json={
                "name": "Test_Register",
                "email": "test.reg@example.com",
                "phone": "+71234567897",
                "password": "Reg!Password123!",
                "confirm_password": "Reg!Password123!"
               }
            )
        print(response)
        assert response.status_code == 200
        assert response.json()["name"] == "Test_Register"
        assert response.json()["email"] == "test.reg@example.com"
        assert response.json()["phone"] == "+71234567897"


@pytest.mark.asyncio
async def test_user_login(test_db):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/users/login",
            json={
                "email": "test.reg@example.com",
                "password": "Reg!Password123!",
            }
        )
        print(response)
        assert response.status_code == 200
        if response.status_code != 200:
            print(response.text)
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_all_users(test_db):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_user_by_id(test_db):
    user_id = 1  # предполагаем, что такой пользователь существует
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



