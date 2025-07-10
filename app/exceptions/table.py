from typing import Self

from fastapi import HTTPException
from fastapi import status


class TableNotFoundException(HTTPException):
    def __init__(self: Self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Столик для удаление не найдено",
        )
