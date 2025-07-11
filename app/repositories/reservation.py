from typing import Self
from typing import Protocol
from typing import Sequence
from typing import Annotated

from fastapi import Depends
from sqlmodel import select
from pydantic import PositiveInt

from app.models.reservation import ReservationModel
from app.exceptions.reservation import ReservationNotFoundException
from app.infrastructure.database import SessionDependency


class ReservationRepositoryProtocol(Protocol):
    """Протокол репозитории брони в ресторане"""

    async def get_reservations(
        self: Self,
    ) -> Sequence[ReservationModel]: ...

    async def delete_reservation(
        self: Self,
        reservation_id: PositiveInt,
    ) -> None: ...


class ReservationRepositoryImpl:
    """Имплементация репозитории брони в ресторане"""

    def __init__(self: Self, session: SessionDependency) -> None:
        self.session = session

    async def get_reservations(
        self: Self,
    ) -> Sequence[ReservationModel]:
        """Получение всех столиков в ресторане"""

        return self.session.exec(select(ReservationModel)).all()

    async def delete_reservation(
        self: Self,
        reservation_id: PositiveInt,
    ) -> None:
        """Удаление брони"""

        db_reservation = self.session.get(ReservationModel, reservation_id)
        if not db_reservation:
            raise ReservationNotFoundException(reservation_id=reservation_id)

        self.session.delete(db_reservation)
        self.session.commit()


async def get_reservation_repository(
    session: SessionDependency,
) -> ReservationRepositoryProtocol:
    return ReservationRepositoryImpl(session=session)


ReservationRepository = Annotated[
    ReservationRepositoryProtocol,
    Depends(get_reservation_repository),
]
