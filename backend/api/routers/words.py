from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from api.cruds import words as word_api
from api.db import get_session
from api.models import words as word_model

router = APIRouter(tags=["words"])


@router.get(
    "/words",
    response_model=List[word_model.WordRead],
    status_code=status.HTTP_200_OK,
)
def read_all_words(*, db: Session = Depends(get_session), spell: str = None):
    if not spell:
        return word_api.get_all_words(db)
    return word_api.filter_by_spell(db, spell)


@router.get(
    "/words/{word_id}",
    response_model=word_model.WordRead,
    status_code=status.HTTP_200_OK,
)
def get_word(*, db: Session = Depends(get_session), word_id: int):
    found = word_api.find_by_id(db, word_id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Word {word_id}: Not Found"
        )
    return found


@router.post(
    "/words",
    response_model=word_model.WordRead,
    status_code=status.HTTP_201_CREATED,
)
def create_word(*, db: Session = Depends(get_session), word: word_model.WordCreate):
    found = word_api.find_by_spell(db, word.spell)
    if found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Word {word.spell} is duplicated"
        )
    return word_api.create_word(db, word)


@router.patch(
    "/words/{word_id}",
    response_model=word_model.WordRead,
    status_code=status.HTTP_200_OK,
)
def update_word(*, db: Session = Depends(get_session), word_id: int, word: word_model.WordUpdate):
    """
    Either word.spell or word.meaning must contain a value.
    """
    # Both spell and meaning which are empty is not allowed
    if not word.spell and not word.meaning:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Word Empty")

    # check wrong word_id
    origin = word_api.find_by_id(db, word_id)
    if not origin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Word {word_id} Not Found"
        )

    # check for duplicate spell in the db
    if word.spell:
        found = word_api.find_by_spell(db, word.spell)
        if found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"Word {word.spell} is duplicated"
            )

    return word_api.update_word(db, origin, word)


@router.delete("/words/{word_id}", response_model=None, status_code=status.HTTP_200_OK)
def delete_word(*, db: Session = Depends(get_session), word_id: int):
    origin = word_api.find_by_id(db, word_id)
    if not origin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Word {word_id} Not Found"
        )
    return word_api.delete_word(db, origin)
