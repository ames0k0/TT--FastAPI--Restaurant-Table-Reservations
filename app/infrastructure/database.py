from typing import Annotated

from app.core.config import settings

from fastapi import Depends
from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine


engine = create_engine(
    url=str(settings.DB__POSTGRES_DSN),
)


def get_session():
    with Session(engine) as session:
        yield session


def create_database_tables():
    SQLModel.metadata.create_all(engine)


def delete_database_tables():
    SQLModel.metadata.drop_all(engine)


SessionDependency = Annotated[Session, Depends(get_session)]
