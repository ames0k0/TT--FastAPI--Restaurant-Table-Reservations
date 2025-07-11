from typing import Annotated
from typing import Sequence

from fastapi import APIRouter
from fastapi import Path
from pydantic import PositiveInt

from app.schemas.reservation import ReservationCreateSchema
from app.schemas.reservation import ReservationOutSchema
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
    reservation: ReservationCreateSchema,
    reservation_service: ReservationService,
):
    """Создаёт бронь"""


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
    """Удаляет бронь"""

    await reservation_service.delete_reservation(reservation_id=reservation_id)
