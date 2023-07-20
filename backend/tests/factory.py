from sqlmodel import Session

from api.models import examples as example_model
from api.models import words as word_model


class WordFactory:
    @staticmethod
    def create_word(db: Session, **kwargs) -> word_model.WordRead:
        word = word_model.WordCreate(**kwargs)
        db_word = word_model.Word.from_orm(word)
        db.add(db_word)
        db.commit()
        db.refresh(db_word)
        return db_word


class ExampleFactory:
    @staticmethod
    def create_example(db: Session, **kwargs) -> example_model.ExampleRead:
        example = example_model.ExampleCreate(**kwargs)
        db_example = example_model.Example.from_orm(example)
        db.add(db_example)
        db.commit()
        db.refresh(db_example)
        return db_example
