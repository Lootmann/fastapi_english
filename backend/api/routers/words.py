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
def read_all_words(*, db: Session = Depends(get_session)):
    return word_api.get_all_words(db)


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
