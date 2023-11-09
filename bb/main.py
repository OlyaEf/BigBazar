import uvicorn
from fastapi import FastAPI

from bb.factory import setup_routes, setup_database

app = FastAPI()

setup_database(app)
setup_routes(app)


if __name__ == '__main__':
    uvicorn.run(
        app="bb.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
