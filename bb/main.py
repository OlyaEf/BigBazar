import uvicorn

from bb.factory import (
    create_app, setup_database, setup_cors,
    setup_routes, custom_openapi,
)

app = create_app()

setup_database(app)
setup_cors(app)
setup_routes(app)

custom_openapi(app)

if __name__ == '__main__':
    uvicorn.run(
        app="bb.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
