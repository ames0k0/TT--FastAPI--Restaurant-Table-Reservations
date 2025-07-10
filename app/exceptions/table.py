from typing import Self

from pydantic import PositiveInt

from fastapi import HTTPException
from fastapi import status


class TableNotFoundException(HTTPException):
    """Ошибка при ненахождение столика по `id`"""

    def __init__(self: Self, table_id: PositiveInt) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Столик по id={table_id} не найдено",
        )
