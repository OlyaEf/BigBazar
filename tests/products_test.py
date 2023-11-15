import pytest

from httpx import AsyncClient
from bb.main import app
from bb.products.models import Product


@pytest.mark.asyncio
async def test_create_product(test_db, register_and_authenticate_user):
    headers = await register_and_authenticate_user
    # Создание продукта
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "price": 100.00
        }
        response = await client.post("/products", json=product_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == product_data["name"]
        # Очистка данных в конце теста
        await Product.all().delete()


@pytest.mark.asyncio
async def test_get_all_products(test_db, register_and_authenticate_user):
    headers = await register_and_authenticate_user
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/products", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        # Очистка данных в конце теста
        await Product.all().delete()


@pytest.mark.asyncio
async def test_partial_update_product_name(test_db, register_and_authenticate_user):
    headers = await register_and_authenticate_user
    # Создать продукт с помощью POST запроса
    async with AsyncClient(app=app, base_url="http://testserver") as client:
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
        # Очистка данных в конце теста
        await Product.all().delete()


@pytest.mark.asyncio
async def test_delete_product(test_db, register_and_authenticate_user):
    headers = await register_and_authenticate_user  # Получаем заголовки из фикстуры
    # Создать продукт с помощью POST запроса
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "price": 100.00
        }

        create_response = await client.post("/products", json=product_data, headers=headers)
        assert create_response.status_code == 200
        product_id = create_response.json()["id"]

        # Удаление продукта
        response = await client.delete(f"/products/{product_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Product deleted successfully"
        # Очистка данных в конце теста
        await Product.all().delete()
