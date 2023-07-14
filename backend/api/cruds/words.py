from typing import List

from sqlmodel import Session, select

from api.models import words as word_model


def get_all_words(db: Session) -> List[word_model.WordRead]:
    return db.exec(select(word_model.Word)).all()


def find_by_id(db: Session, word_id: int) -> word_model.WordRead | None:
    stmt = select(word_model.Word).where(word_model.Word.id == word_id)
    return db.exec(stmt).first()


def filter_by_spell(db: Session, spell: str) -> List[word_model.WordRead]:
    # FIXME: There has to be a better way :^)
    stmt = select(word_model.Word).filter(word_model.Word.spell.ilike(f"%{spell}%"))
    return db.exec(stmt).all()


def find_by_spell(db: Session, spell: str) -> word_model.WordRead | None:
    stmt = select(word_model.Word).where(word_model.Word.spell == spell.lower())
    return db.exec(stmt).first()


def create_word(db: Session, word: word_model.Word) -> word_model.WordRead:
    db_word = word_model.Word.from_orm(word)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def update_word(db: Session, origin: word_model.Word, word: word_model.Word) -> word_model.WordRead:
    if word.spell is not None:
        origin.spell = word.spell

    if word.meaning is not None:
        origin.meaning = word.meaning

    db.add(origin)
    db.commit()
    db.refresh(origin)

    return origin


def delete_word(db: Session, origin: word_model.Word) -> None:
    db.delete(origin)
    db.commit()
