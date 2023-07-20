"""
Word : Example = 1 : n
"""
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.examples import Example


class WordBase(SQLModel):
    spell: str = Field(index=True)
    meaning: str = Field(index=True)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "sentence": "hello world",
                "translation": "こんにちは、せかい。",
                "word_id": "1",
            }
        }


class Word(WordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    examples: List["Example"] = Relationship(back_populates="word")


class WordCreate(WordBase):
    pass


class WordRead(WordBase):
    id: int


class WordUpdate(SQLModel):
    spell: Optional[str] = None
    meaning: Optional[str] = None
