from datetime import datetime

from sqlmodel import SQLModel
from sqlmodel import Field


class ReservationModel(SQLModel, table=True):
    """Модель бронь в ресторане"""

    __tablename__ = "reservation"  # type: ignore

    id: int = Field(primary_key=True, description="ID бронирования")

    customer_name: str = Field(description="Имя клиента")
    reservation_time: datetime = Field(description="Время резервирования")
    duration_minutes: int = Field(
        description="Продолжительность резервирования в минутах",
    )

    # -- Relations
    table_id: int = Field(foreign_key="table.id", description="ID столика")
