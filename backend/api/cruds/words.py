from typing import List

from sqlmodel import Session, select

from api.models import words as word_model


def get_all_words(db: Session) -> List[word_model.WordRead]:
    return db.exec(select(word_model.Word)).all()
