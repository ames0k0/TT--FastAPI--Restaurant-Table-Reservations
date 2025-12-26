from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import Field
from pydantic import FutureDatetime
from sqlmodel import Session
from sqlmodel import select

from app.infrastructure.database import get_session
from app.models.table import TableModel
from app.models.reservation import ReservationModel
from app.exceptions.table import TableNotFoundException
from app.exceptions.reservation import ReservationTimeConflictException


class ReservationBaseSchema(BaseModel):
    """Базовая схема бронирование столика в ресторане"""

    customer_name: str = Field(description="Имя клиента")
    reservation_time: FutureDatetime = Field(
        description="Время резервирования",
    )
    duration_minutes: PositiveInt = Field(
        description="Продолжительность резервирования в минутах"
    )
    table_id: PositiveInt = Field(description="ID столика")


class ReservationCreateSchema(ReservationBaseSchema):
    """Схема создание бронирования столика в ресторане"""


class ReservationOutSchema(ReservationBaseSchema):
    """Схема получение брони в ресторане"""

    id: PositiveInt = Field(description="ID бронирования")


# XXX (ames0k0): No `utils.py` yet
def minutes_to_seconds(minutes: PositiveInt):
    return minutes * 60


def reservation_create_validate(
    reservation: ReservationCreateSchema,
) -> ReservationCreateSchema:
    """Валидация брони на уровни API ?!!"""

    new_reservation_tis = int(
        reservation.reservation_time.timestamp(),
    )
    new_reservation_time_range = range(
        new_reservation_tis,
        new_reservation_tis + minutes_to_seconds(reservation.duration_minutes),
    )

    session: Session = next(get_session())

    db_table = session.get(TableModel, reservation.table_id)
    if not db_table:
        raise TableNotFoundException(table_id=reservation.table_id)

    db_reservations = session.exec(
        select(ReservationModel).where(
            ReservationModel.table_id == reservation.table_id,
        )
    ).all()

    for db_reservation in db_reservations:
        db_reservation_tis = int(db_reservation.reservation_time.timestamp())
        db_reservation_dis = db_reservation_tis + minutes_to_seconds(
            db_reservation.duration_minutes
        )

        if any(
            (
                db_reservation_tis in new_reservation_time_range,
                db_reservation_dis in new_reservation_time_range,
            )
        ):
            raise ReservationTimeConflictException(
                db_reservation=db_reservation,
            )

    return reservation
