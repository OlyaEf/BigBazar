from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from tortoise.contrib.fastapi import register_tortoise

from bb.core import config
from bb.products.routes import products_router


def create_app():
    application = FastAPI()
    return application


def setup_database(application: FastAPI) -> None:
    register_tortoise(
        application,
        db_url=config.DATABASE_URL,
        modules={"models": [*config.MODELS]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


def setup_cors(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_routes(application: FastAPI) -> None:
    application.include_router(products_router)


def custom_openapi(application: FastAPI) -> Dict[str, dict]:
    if application.openapi_schema:
        return application.openapi_schema
    openapi_schema = get_openapi(
        title="API BigBazar",
        version="1.0.0",
        summary="API для разработчиков в сфере электронной коммерции",
        description="**API BigBazar** это инструмент, который "
                    "позволяет разработчикам интегрировать функциональность"
                    " электронной коммерции, такую как управление товарами, "
                    "контроль запасов, обработка заказов и управление данными "
                    "клиентов, в свои приложения или веб-сайты, "
                    "что делает запуск онлайн-магазинов более простым.",
        routes=application.routes,
        terms_of_service="",
        contact={
            "name": "Olga Efimovskikh - Backend Developer",
            "url": "https://github.com/OlyaEf",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    application.openapi_schema = openapi_schema
    return application.openapi_schema
