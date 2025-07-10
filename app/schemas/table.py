from pydantic import BaseModel


class TableBaseSchema(BaseModel):
    name: str
    seats: int
    location: str


class TableCreateSchema(TableBaseSchema):
    pass


class TableOutSchema(TableBaseSchema):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
