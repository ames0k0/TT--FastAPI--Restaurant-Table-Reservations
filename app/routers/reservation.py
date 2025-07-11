# from typing import Annotated
from typing import Sequence

from fastapi import APIRouter
# from fastapi import Path

# from app.schemas.reservation import ReservationCreateSchema
from app.schemas.reservation import ReservationOutSchema
from app.services.reservation import ReservationService


reservation_router = APIRouter()


@reservation_router.get("/", response_model=Sequence[ReservationOutSchema])
async def get_reservations(
    reservation_service: ReservationService,
):
    """Возвращает список всех броней"""
    reservations = await reservation_service.get_reservations()
    print(">>>", reservations)
    return reservations
