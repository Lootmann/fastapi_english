from typing import List

from fastapi import APIRouter, Depends, status
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
