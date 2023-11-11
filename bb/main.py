import uvicorn
from fastapi import FastAPI

from bb.factory import setup_routes, setup_database
from bb.users.routes import users_router

app = FastAPI()

setup_database(app)
setup_routes(app)

# подключение роутеров
app.include_router(users_router, prefix="", tags=["users"])


if __name__ == '__main__':
    uvicorn.run(
        app="bb.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
