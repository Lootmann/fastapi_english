from sqlmodel import Session, create_engine

from api.models.examples import Example
from api.models.words import Word

sqlite_file_name = "dev.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    Word.metadata.drop_all(engine)
    Word.metadata.create_all(engine)

    Example.metadata.drop_all(engine)
    Example.metadata.create_all(engine)
