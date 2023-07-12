from sqlmodel import Session

from api.models import words as word_model


class WordFactory:
    @staticmethod
    def create_word(db: Session, **kwargs) -> word_model.WordRead:
        word = word_model.WordCreate(**kwargs)
        db_word = word_model.Word.from_orm(word)
        db.add(db_word)
        db.commit()
        db.refresh(db_word)
