from sqlmodel import Field, SQLModel


class TableModel(SQLModel, table=True):
    """Модель стола в ресторане"""

    id: int = Field(..., primary_key=True)
    name: str = Field(..., description="")
    seats: int = Field(..., index=True)
    location: str
