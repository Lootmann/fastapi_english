from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from api.cruds import examples as example_api
from api.db import get_session
from api.models import examples as example_model

router = APIRouter(tags=["examples"])


@router.get(
    "/examples",
    response_model=List[example_model.ExampleRead],
    status_code=status.HTTP_200_OK,
)
def read_all_examples(*, db: Session = Depends(get_session)):
    return example_api.get_all_examples(db)


@router.get(
    "/examples/{example_id}",
    response_model=example_model.ExampleRead,
    status_code=status.HTTP_200_OK,
)
def get_example(*, db: Session = Depends(get_session), example_id: int):
    found = example_api.find_by_id(db, example_id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Example {example_id} Not Found"
        )
    return found
