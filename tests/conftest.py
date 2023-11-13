import pytest
from tortoise import Tortoise

from bb.core.config import MODELS, POSTGRES_PASSWORD, \
    POSTGRES_HOST, POSTGRES_PORT

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
