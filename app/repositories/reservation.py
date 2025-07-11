from typing import Self
from typing import Protocol
from typing import Sequence
from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from app.models.reservation import ReservationModel
from app.infrastructure.database import SessionDependency


class ReservationRepositoryProtocol(Protocol):
    """Протокол репозитории брони в ресторане"""

    async def get_reservations(
        self: Self,
    ) -> Sequence[ReservationModel]: ...


class ReservationRepositoryImpl:
    """Имплементация репозитории брони в ресторане"""

    def __init__(self: Self, session: SessionDependency) -> None:
        self.session = session

    async def get_reservations(
        self: Self,
    ) -> Sequence[ReservationModel]:
        """Получение всех столиков в ресторане"""
        return self.session.exec(select(ReservationModel)).all()


async def get_reservation_repository(
    session: SessionDependency,
) -> ReservationRepositoryProtocol:
    return ReservationRepositoryImpl(session=session)


ReservationRepository = Annotated[
    ReservationRepositoryProtocol,
    Depends(get_reservation_repository),
]
