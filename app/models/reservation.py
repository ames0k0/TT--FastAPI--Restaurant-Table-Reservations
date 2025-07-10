from datetime import datetime

from sqlmodel import Field
from sqlmodel import SQLModel


class ReservationModel(SQLModel, table=True):
    """Модель бронь в ресторане"""

    __tablename__ = "reservation"  # type: ignore

    id: int = Field(..., primary_key=True, description="TODO")

    customer_name: str = Field(..., description="TODO")
    reservation_time: datetime = Field(..., description="TODO")
    duration_time: int = Field(..., description="TODO")

    # -- Relations
    table_id: int = Field(..., foreign_key="table.id", description="TODO")
