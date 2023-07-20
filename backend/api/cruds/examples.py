from typing import List

from sqlmodel import Session, select

from api.models import examples as example_model


def get_all_examples(db: Session) -> List[example_model.ExampleRead]:
    return db.exec(select(example_model.Example)).all()


def find_by_id(db: Session, example_id: int) -> example_model.ExampleRead | None:
    stmt = select(example_model.Example).where(example_model.Example.id == example_id)
    return db.exec(stmt).first()


def create_example(db: Session, example: example_model.Example) -> example_model.ExampleRead:
    db_example = example_model.Example.from_orm(example)
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example
