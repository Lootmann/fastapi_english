"""
Word : Example = 1 : n
"""
from typing import Optional

from sqlmodel import Field, SQLModel


class WordBase(SQLModel):
    spell: str = Field(index=True)
    meaning: str = Field(index=True)


class Word(WordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class WordCreate(WordBase):
    pass


class WordRead(WordBase):
    id: int


class WordUpdate(SQLModel):
    spell: Optional[str] = None
    meaning: Optional[str] = None
