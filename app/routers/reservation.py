from typing import Annotated
from typing import Sequence

from fastapi import APIRouter
from fastapi import Path
from pydantic import PositiveInt
from pydantic import AfterValidator

from app.schemas.reservation import ReservationCreateSchema
from app.schemas.reservation import ReservationOutSchema
from app.schemas.reservation import reservation_create_validate
from app.services.reservation import ReservationService


reservation_router = APIRouter()


@reservation_router.get("/", response_model=Sequence[ReservationOutSchema])
async def get_reservations(
    reservation_service: ReservationService,
):
    """Возвращает список всех броней"""

    return await reservation_service.get_reservations()


@reservation_router.post("/", response_model=ReservationOutSchema)
async def create_reservation(
    reservation: Annotated[
        ReservationCreateSchema, AfterValidator(reservation_create_validate)
    ],
    reservation_service: ReservationService,
):
    """Создаёт бронь"""

    return await reservation_service.create_reservation(
        reservation=reservation,
    )


@reservation_router.delete("/{id}")
async def delete_reservation(
    reservation_id: Annotated[
        PositiveInt,
        Path(
            description="ID брони",
            alias="id",
        ),
    ],
    reservation_service: ReservationService,
):
    """Удаляет бронь по `id`,

    выбрасывает исключение при отсутствие брони"""

    await reservation_service.delete_reservation(reservation_id=reservation_id)
