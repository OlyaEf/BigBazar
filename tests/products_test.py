import pytest

from httpx import AsyncClient
from bb.main import app
from bb.products.models import Product


@pytest.mark.asyncio
async def register_and_authenticate_user(client):
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


@pytest.mark.asyncio
async def test_create_product(test_db):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        headers = await register_and_authenticate_user(client)

        # Создание продукта
        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "price": 100.00
        }
        response = await client.post("/products", json=product_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == product_data["name"]


@pytest.mark.asyncio
async def test_get_all_products(test_db):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        headers = await register_and_authenticate_user(client)

        response = await client.get("/products", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_partial_update_product_name(test_db):
    # Создать продукт с помощью POST запроса
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        headers = await register_and_authenticate_user(client)

        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "price": 100.00
        }

        create_response = await client.post("/products", json=product_data, headers=headers)
        assert create_response.status_code == 200

        product_id = create_response.json()["id"]

        # Обновить только имя продукта с помощью PATCH запроса
        updated_data = {"name": "Updated Product Name"}

        response = await client.patch(f"/products/{product_id}", json=updated_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == updated_data["name"]

        # Проверить, что остальные поля остались неизменными
        updated_product = await Product.get(id=product_id)
        assert updated_product.description == product_data["description"]
        assert updated_product.price == product_data["price"]


@pytest.mark.asyncio
async def test_delete_product(test_db):
    # ID продукта для удаления
    product_id = 1
    access_token = "your_access_token"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        headers = await register_and_authenticate_user(client)

        response = await client.delete(f"/products/{product_id}", headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "Product deleted successfully"
