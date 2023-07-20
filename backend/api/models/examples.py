"""
Word : Example = 1 : n
"""
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.words import Word


class ExampleBase(SQLModel):
    sentence: str = Field(index=True)
    translation: str = Field(index=True)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "sentence": "hello world",
                "translation": "こんにちは、せかい。",
                "word_id": "1",
            }
        }


class Example(ExampleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    word_id: Optional[int] = Field(default=None, foreign_key="word.id")
    word: Optional["Word"] = Relationship(back_populates="examples")


class ExampleCreate(ExampleBase):
    sentence: str = ""
    translation: str = ""
    word_id: Optional[int] = Field(default=None, foreign_key="word.id")


class ExampleRead(ExampleBase):
    id: int
    word_id: Optional[int] = Field(default=None, foreign_key="word.id")


class ExampleUpdate(SQLModel):
    pass
