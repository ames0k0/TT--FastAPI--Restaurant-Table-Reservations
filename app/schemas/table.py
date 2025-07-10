from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import ConfigDict
from pydantic import Field


class TableBaseSchema(BaseModel):
    """Базовая схема столика в ресторане"""

    name: str = Field(..., description="Название столика")
    seats: PositiveInt = Field(..., description="Количество мест за столиком")
    location: str = Field(..., description="Расположение столика")


class TableCreateSchema(TableBaseSchema):
    """Схема создание столика в ресторане"""


class TableOutSchema(TableBaseSchema):
    """Схема получение столика в ресторане"""

    id: PositiveInt = Field(..., description="ID столика")

    model_config = ConfigDict(from_attributes=True)
