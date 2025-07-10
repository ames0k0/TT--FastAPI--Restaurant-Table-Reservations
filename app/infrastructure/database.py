from typing import Annotated

from app.core.config import settings

from fastapi import Depends
from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine


engine = create_engine(
    url=str(settings.POSTGRES_DSN),
)


def get_session():
    with Session(engine) as session:
        yield session


SQLModel.metadata.create_all(engine)


SessionDependency = Annotated[Session, Depends(get_session)]
