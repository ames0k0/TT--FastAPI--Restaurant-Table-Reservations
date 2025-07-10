from typing import Self
from typing import Protocol
from typing import Sequence
from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from app.models.table import TableModel
from app.schemas.table import TableCreateSchema
from app.infrastructure.database import SessionDependency
from app.exceptions.table import TableNotFoundException


class TableRepositoryProtocol(Protocol):
    """TODO"""

    async def get_tables(
        self: Self,
        session: SessionDependency,
    ) -> Sequence[TableModel]: ...

    async def create_table(
        self: Self,
        table: TableCreateSchema,
        session: SessionDependency,
    ) -> TableModel: ...

    async def delete_table(
        self: Self,
        table_id: int,
        session: SessionDependency,
    ) -> None: ...


class TableRepositoryImpl:
    async def get_tables(
        self: Self,
        session: SessionDependency,
    ) -> Sequence[TableModel]:
        return session.exec(select(TableModel)).all()

    async def create_table(
        self: Self,
        table: TableCreateSchema,
        session: SessionDependency,
    ) -> TableModel:
        new_table = TableModel(**table.model_dump())

        session.add(new_table)
        session.commit()
        session.refresh(new_table)

        return new_table

    async def delete_table(
        self: Self,
        table_id: int,
        session: SessionDependency,
    ) -> None:
        db_table = session.get(TableModel, table_id)
        if not db_table:
            raise TableNotFoundException()
        session.delete(db_table)
        session.commit()


async def get_table_repository() -> TableRepositoryProtocol:
    return TableRepositoryImpl()


TableRepository = Annotated[
    TableRepositoryProtocol,
    Depends(get_table_repository),
]
