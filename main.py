from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.infrastructure.database import create_database_tables
from app.routers.table import table_router
from app.routers.reservation import reservation_router


@asynccontextmanager
async def lifespan(_):
    create_database_tables()
    yield


app = FastAPI(
    title=settings.APP__TITLE,
    description=settings.APP__DESCRIPTION,
    debug=settings.SYSTEM.APP__DEBUG,
    lifespan=lifespan,
)


app.include_router(
    table_router,
    prefix="/tables",
    tags=["tables"],
)
app.include_router(
    reservation_router,
    prefix="/reservations",
    tags=["reservations"],
)


@app.get("/", tags=["index"], response_model=dict)
async def read_root():
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
