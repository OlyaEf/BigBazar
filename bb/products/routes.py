from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from bb.products.schemas import ProductRetrieveSchema, ProductCreateUpdateSchema, ProductPartialUpdateSchema
from bb.products.services import ProductService
from bb.security.auth import get_current_user

products_router = APIRouter()


@products_router.post("/products", response_model=ProductRetrieveSchema)
async def create_product(product_data: ProductCreateUpdateSchema, current_user=Depends(get_current_user)):
    """
    Создание нового продукта. Доступно только авторизованным пользователям.
    """
    product = await ProductService.create_product(product_data, owner_id=current_user.id)
    return product


@products_router.patch("/products/{product_id}", response_model=ProductRetrieveSchema)
async def update_product(product_id: int, product_data: ProductPartialUpdateSchema, current_user=Depends(get_current_user)):
    """
    Обновление данных продукта. Доступно только авторизованным пользователям.
    """
    product = await ProductService.update_product(product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id: int, current_user=Depends(get_current_user)):
    """
    Удаление продукта. Доступно только авторизованным пользователям.
    """
    success = await ProductService.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


@products_router.get("/products", response_model=List[ProductRetrieveSchema])
async def list_products(limit: int = Query(10, gt=0), offset: int = Query(0, gt=0), current_user=Depends(get_current_user)):
    """
    Получение списка активных продуктов. Доступно всем пользователям.
    """
    products = await ProductService.get_active_products(limit, offset)
    return products
