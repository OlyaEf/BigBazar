from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from bb.core.config import DATABASE_URL, MODELS
from bb.users.routes import users_router
from bb.products.routes import products_router


def setup_database(app: FastAPI) -> None:
    """
    Настраивает подключение к базе данных.

    Parameters:
        - app (FastAPI): Экземпляр FastAPI приложения.

    Returns:
        - None
    """
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={
            "models": [*MODELS],
        },
        generate_schemas=True,
    )


def setup_routes(app: FastAPI) -> None:
    """
    Настраивает маршруты приложения.

    Parameters:
        - app (FastAPI): Экземпляр FastAPI приложения.

    Returns:
        - None
    """
    app.include_router(users_router, prefix="/users", tags=["users"])
    app.include_router(products_router, prefix="", tags=["products"])
