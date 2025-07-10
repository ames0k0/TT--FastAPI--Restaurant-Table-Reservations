from typing import Annotated
from typing import Sequence

from fastapi import APIRouter
from fastapi import Path

from app.models.table import TableModel
from app.schemas.table import TableCreateSchema
from app.schemas.table import TableOutSchema
from app.services.table import TableService
from app.infrastructure.database import SessionDependency


table_router = APIRouter()


@table_router.get("/", response_model=Sequence[TableOutSchema])
async def get_tables(
    session: SessionDependency,
    table_service: TableService,
):
    """Возвращает список всех столиков"""
    tables = await table_service.get_tables(session=session)
    print(tables)
    return tables


@table_router.post("/", response_model=TableOutSchema)
async def create_table(
    table: TableCreateSchema,
    session: SessionDependency,
    table_service: TableService,
):
    """Создаёт нового столика"""
    db_table = await table_service.create_table(
        session=session,
        table=table,
    )
    print("??", db_table)
    return db_table


@table_router.delete("/{id}", response_model=None)
async def delete_table(
    table_id: Annotated[int, Path(title="TODO", alias="id")],
    session: SessionDependency,
    table_service: TableService,
):
    """Удаляет столика по `id`,

    выбрасывает исключение при отсутствие столика"""
    await table_service.delete_table(
        table_id=table_id,
        session=session,
    )
