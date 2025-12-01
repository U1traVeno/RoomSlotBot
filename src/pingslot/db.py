from sqlmodel import SQLModel, create_engine
from pingslot.config import settings

engine = create_engine(settings.database.url, echo=settings.database.echo)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    from sqlmodel import Session
    with Session(engine) as session:
        yield session
