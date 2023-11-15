import pytest
from httpx import AsyncClient
from bb.main import app
from bb.products.models import Product


# Создание продукта
@pytest.mark.asyncio
async def test_create_product(test_db, authenticated_user_token):
    async with authenticated_user_token as headers:  # headers предоставляются здесь
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


# Получение списка продуктов
@pytest.mark.asyncio
async def test_get_all_products(test_db, authenticated_user_token):
    async with authenticated_user_token as headers:
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/products", headers=headers)
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        # Очистка данных в конце теста
        await Product.all().delete()


# Частичное обновление продукта
@pytest.mark.asyncio
async def test_partial_update_product_name(test_db, authenticated_user_token):
    async with authenticated_user_token as headers:
        # Создать продукт
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            product_data = {
                "name": "Test Product",
                "description": "A test product description",
                "price": 100.00
            }
            create_response = await client.post("/products", json=product_data, headers=headers)
            product_id = create_response.json()["id"]
            # Обновить продукт
            updated_data = {"name": "Updated Product Name"}
            response = await client.patch(f"/products/{product_id}", json=updated_data, headers=headers)
            assert response.status_code == 200
            assert response.json()["name"] == updated_data["name"]
        # Очистка данных в конце теста
        await Product.filter(id=product_id).delete()


# Удаление продукта
@pytest.mark.asyncio
async def test_delete_product(test_db, authenticated_user_token):
    async with authenticated_user_token as headers:
        # Создать продукт
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            product_data = {
                "name": "Test Product",
                "description": "A test product description",
                "price": 100.00
            }
            create_response = await client.post("/products", json=product_data, headers=headers)
            product_id = create_response.json()["id"]
            # Удалить продукт
            response = await client.delete(f"/products/{product_id}", headers=headers)
            assert response.status_code == 200
            assert response.json()["message"] == "Product deleted successfully"
        # Очистка данных в конце теста
        await Product.filter(id=product_id).delete()


# Получение активных продуктов
@pytest.mark.asyncio
async def test_get_only_active_productss(test_db, authenticated_user_token):
    async with authenticated_user_token as headers:
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Создаем активные и неактивные продукты
            for i in range(5):
                await client.post("/products", json={
                    "name": f"Active Product {i}",
                    "description": "Active Description",
                    "price": 100.00,
                    "is_active": True
                }, headers=headers)
                await client.post("/products", json={
                    "name": f"Inactive Product {i}",
                    "description": "Inactive Description",
                    "price": 100.00,
                    "is_active": False
                }, headers=headers)

            # Получаем список продуктов
            response = await client.get("/products", headers=headers)
            products = response.json()
            assert response.status_code == 200
            assert len(products) <= 5  # Убедитесь, что количество продуктов соответствует ожидаемому
            assert all(product['is_active'] for product in products)

            # Очистка данных в конце теста
            await Product.all().delete()
