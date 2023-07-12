from typing import List

from sqlmodel import Session, select

from api.models import words as word_model


def get_all_words(db: Session) -> List[word_model.WordRead]:
    return db.exec(select(word_model.Word)).all()


def find_by_id(db: Session, word_id: int) -> word_model.WordRead | None:
    stmt = select(word_model.Word).where(word_model.Word.id == word_id)
    return db.exec(stmt).first()
