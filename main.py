import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.routers.table import table_router


app = FastAPI(
    title=settings.APP__TITLE,
    description=settings.APP__DESCRIPTION,
    debug=settings.SYSTEM.APP__DEBUG,
)


app.include_router(table_router, prefix="/tables", tags=["tables"])


@app.get("/", tags=["index"], response_model=dict)
def read_root():
    """Энтрипоинт для получение доступных эндпоинтов"""

    return {
        "routers": [
            {"name": "Столики", "prefix": "/tables"},
            {"name": "Брони", "prefix": "/reservations"},
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        app=settings.SYSTEM.UVICORN__APP,
        host=settings.SYSTEM.UVICORN__HOST,
        port=settings.SYSTEM.UVICORN__PORT,
        reload=bool(settings.SYSTEM.UVICORN__RELOAD),
    )
