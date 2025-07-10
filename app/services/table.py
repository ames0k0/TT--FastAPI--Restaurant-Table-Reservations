from typing import Annotated
from typing import Protocol
from typing import Self
from typing import Sequence

from fastapi import Depends

from app.models.table import TableModel
from app.schemas.table import TableCreateSchema
from app.repositories.table import TableRepository, TableRepositoryProtocol


class TableServiceProtocol(Protocol):
    """TODO"""

    async def get_tables(
        self: Self,
    ) -> Sequence[TableModel]: ...

    async def create_table(
        self: Self,
        table: TableCreateSchema,
    ) -> TableModel: ...

    async def delete_table(
        self: Self,
        table_id: int,
    ) -> None: ...


class TableServiceImpl:
    def __init__(
        self: Self,
        repository: TableRepositoryProtocol,
    ) -> None:
        self.repository = repository

    async def get_tables(
        self: Self,
    ) -> Sequence[TableModel]:
        return await self.repository.get_tables()

    async def create_table(
        self: Self,
        table: TableCreateSchema,
    ) -> TableModel:
        return await self.repository.create_table(table=table)

    async def delete_table(
        self: Self,
        table_id: int,
    ) -> None:
        await self.repository.delete_table(table_id=table_id)


async def get_table_service(
    repository: TableRepository,
) -> TableServiceProtocol:
    return TableServiceImpl(repository=repository)


TableService = Annotated[TableServiceProtocol, Depends(get_table_service)]
