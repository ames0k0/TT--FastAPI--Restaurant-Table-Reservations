from sqlmodel import Field, SQLModel


class TableModel(SQLModel, table=True):
    """Модель столика в ресторане"""

    __tablename__ = "table"  # type: ignore

    id: int = Field(..., primary_key=True, description="ID столика")
    name: str = Field(..., description="Название столика")
    seats: int = Field(..., description="Количество мест за столиком")
    location: str = Field(..., description="Расположение столика")
