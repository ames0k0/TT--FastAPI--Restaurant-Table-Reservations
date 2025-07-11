from typing import Annotated
from typing import Protocol
from typing import Self
from typing import Sequence

from fastapi import Depends
from pydantic import PositiveInt

from app.models.reservation import ReservationModel
from app.schemas.reservation import ReservationCreateSchema
from app.repositories.reservation import ReservationRepositoryProtocol
from app.repositories.reservation import ReservationRepository


class ReservationServiceProtocol(Protocol):
    """Протокол сервиса брони в ресторане"""

    async def get_reservations(
        self: Self,
    ) -> Sequence[ReservationModel]: ...

    async def create_reservation(
        self: Self,
        reservation: ReservationCreateSchema,
    ) -> ReservationModel: ...

    async def delete_reservation(
        self: Self,
        reservation_id: PositiveInt,
    ) -> None: ...


class ReservationServiceImpl:
    """Имплементация сервиса брони в ресторане"""

    def __init__(
        self: Self,
        repository: ReservationRepositoryProtocol,
    ) -> None:
        self.repository = repository

    async def get_reservations(self: Self) -> Sequence[ReservationModel]:
        return await self.repository.get_reservations()

    async def create_reservation(
        self: Self,
        reservation: ReservationCreateSchema,
    ) -> ReservationModel:
        return await self.repository.create_reservation(
            reservation=reservation,
        )

    async def delete_reservation(
        self: Self,
        reservation_id: PositiveInt,
    ) -> None:
        await self.repository.delete_reservation(reservation_id=reservation_id)


def get_reservation_service(
    repository: ReservationRepository,
) -> ReservationServiceProtocol:
    return ReservationServiceImpl(repository=repository)


ReservationService = Annotated[
    ReservationServiceProtocol, Depends(get_reservation_service)
]
