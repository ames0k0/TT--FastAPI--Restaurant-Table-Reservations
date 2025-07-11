from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import Field
from pydantic import NaiveDatetime


class ReservationBaseSchema(BaseModel):
    """Базовая схема бронирование столика в ресторане"""

    customer_name: str = Field(description="Имя клиента")
    reservation_time: NaiveDatetime = Field(description="Время резервирования")
    duration_minutes: PositiveInt = Field(
        description="Продолжительность резервирования в минутах"
    )
    table_id: PositiveInt = Field(description="ID столика")


class ReservationCreateSchema(ReservationBaseSchema):
    """Схема создание бронирования столика в ресторане"""


class ReservationOutSchema(ReservationBaseSchema):
    """Схема получение брони в ресторане"""

    id: PositiveInt = Field(description="ID бронирования")
