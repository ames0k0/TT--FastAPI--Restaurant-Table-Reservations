from typing import Annotated
from typing import Protocol
from typing import Self
from typing import Sequence

from fastapi import Depends

from app.models.reservation import ReservationModel
from app.repositories.reservation import ReservationRepositoryProtocol
from app.repositories.reservation import ReservationRepository


class ReservationServiceProtocol(Protocol):
    """Протокол сервиса брони в ресторане"""

    async def get_reservations(self: Self) -> Sequence[ReservationModel]: ...


class ReservationServiceImpl:
    """Имплементация сервиса брони в ресторане"""

    def __init__(
        self: Self,
        repository: ReservationRepositoryProtocol,
    ) -> None:
        self.repository = repository

    async def get_reservations(self: Self) -> Sequence[ReservationModel]:
        return await self.repository.get_reservations()


def get_reservation_service(
    repository: ReservationRepository,
) -> ReservationServiceProtocol:
    return ReservationServiceImpl(repository=repository)


ReservationService = Annotated[
    ReservationServiceProtocol, Depends(get_reservation_service)
]
