import uvicorn
from fastapi import FastAPI

from app.routers.table import table_router


# TODO (ames0k0): Remove debug
app = FastAPI(title="Modular FastAPI App", debug=True)


app.include_router(table_router, prefix="/tables", tags=["tables"])


@app.get("/", tags=["index"])
def read_root():
    return {
        "routers": [
            {
                "name": "Столики",
                "prefix": "/tables",
            },
            {
                "name": "Брони",
                "prefix": "/reservations",
            },
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True,
    )
