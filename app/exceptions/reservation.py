from typing import Self

from pydantic import PositiveInt

from fastapi import HTTPException
from fastapi import status

from app.models.reservation import ReservationModel


class ReservationNotFoundException(HTTPException):
    """Ошибка при ненахождение брони по `id`"""

    def __init__(self: Self, reservation_id: PositiveInt) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бронь по id={reservation_id} не найдено",
        )


class ReservationTimeConflictException(HTTPException):
    """Ошибка при конфликта брони по времени"""

    def __init__(self: Self, db_reservation: ReservationModel) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Нельзя создать бронь, "
                "указанный временной слот столик уже занят",
                "reservation_id": db_reservation.id,
            },
        )
