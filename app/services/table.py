from typing import Annotated
from typing import Protocol
from typing import Self
from typing import Sequence

from fastapi import Depends

from app.models.table import TableModel
from app.schemas.table import TableCreateSchema
from app.repositories.table import TableRepository, TableRepositoryProtocol
from app.infrastructure.database import SessionDependency


class TableServiceProtocol(Protocol):
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
    ) -> TableModel: ...


class TableServiceImpl:
    def __init__(
        self: Self,
        repository: TableRepositoryProtocol,
    ) -> None:
        self.repository = repository

    async def get_tables(
        self: Self,
        session: SessionDependency,
    ) -> Sequence[TableModel]:
        return await self.repository.get_tables(session=session)

    async def create_table(
        self: Self,
        table: TableCreateSchema,
        session: SessionDependency,
    ) -> TableModel:
        return await self.repository.create_table(table=table, session=session)

    async def delete_table(
        self: Self,
        table_id: int,
        session: SessionDependency,
    ) -> None:
        await self.repository.delete_table(table_id=table_id, session=session)


async def get_table_service(
    repository: TableRepository,
) -> TableServiceProtocol:
    return TableServiceImpl(repository=repository)


TableService = Annotated[TableServiceProtocol, Depends(get_table_service)]
