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
    """Протокол репозитории столика в ресторане"""

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


class TableRepositoryImpl:
    """Имплементация репозитории столика в ресторане"""

    def __init__(self: Self, session: SessionDependency) -> None:
        self.session = session

    async def get_tables(
        self: Self,
    ) -> Sequence[TableModel]:
        """Получение всех столиков в ресторане"""
        return self.session.exec(select(TableModel)).all()

    async def create_table(
        self: Self,
        table: TableCreateSchema,
    ) -> TableModel:
        """Создание столика в ресторане"""
        new_table = TableModel(**table.model_dump())

        self.session.add(new_table)
        self.session.commit()
        self.session.refresh(new_table)

        return new_table

    async def delete_table(
        self: Self,
        table_id: int,
    ) -> None:
        """Удаление столика из ресторана"""
        db_table = self.session.get(TableModel, table_id)
        if not db_table:
            raise TableNotFoundException(table_id=table_id)
        self.session.delete(db_table)
        self.session.commit()


async def get_table_repository(
    session: SessionDependency,
) -> TableRepositoryProtocol:
    return TableRepositoryImpl(session=session)


TableRepository = Annotated[
    TableRepositoryProtocol,
    Depends(get_table_repository),
]
