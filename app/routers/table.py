from typing import Annotated
from typing import Sequence

from fastapi import APIRouter
from fastapi import Path
from pydantic import PositiveInt

from app.schemas.table import TableCreateSchema
from app.schemas.table import TableOutSchema
from app.services.table import TableService


table_router = APIRouter()


@table_router.get("/", response_model=Sequence[TableOutSchema])
async def get_tables(
    table_service: TableService,
):
    """Возвращает список всех столиков"""

    return await table_service.get_tables()


@table_router.post("/", response_model=TableOutSchema)
async def create_table(
    table: TableCreateSchema,
    table_service: TableService,
):
    """Создаёт нового столика"""

    return await table_service.create_table(table=table)


@table_router.delete("/{id}", response_model=None)
async def delete_table(
    table_id: Annotated[
        PositiveInt,
        Path(
            description="ID столика",
            alias="id",
        ),
    ],
    table_service: TableService,
):
    """Удаляет столика по `id`,

    выбрасывает исключение при отсутствие столика"""

    await table_service.delete_table(table_id=table_id)
