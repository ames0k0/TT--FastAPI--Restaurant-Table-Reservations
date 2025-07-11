from typing import Self

from pydantic import PositiveInt

from fastapi import HTTPException
from fastapi import status


class ReservationNotFoundException(HTTPException):
    """Ошибка при ненахождение брони по `id`"""

    def __init__(self: Self, reservation_id: PositiveInt) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бронь по id={reservation_id} не найдено",
        )
