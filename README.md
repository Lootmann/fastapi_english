# Word Power made Easy

## Overview

## Envs

## Backend

- [FastAPI](https://github.com/tiangolo/fastapi)
- [SQLModel](https://github.com/tiangolo/sqlmodel)

## Frontend

## Models

```python
class Words:
  spell:str
  meaning:str

class Examples:
  sentence: str
  translation: str
  word: ForeignKey
```
