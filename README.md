# Word Power made Easy

## Overview

## Envs

- packages
  - fastapi
  - uvicorn
  - pytest
  - coverage
  - sqlmodel

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

## Tips

1. PUT vs PATCH
   https://qiita.com/murata0705/items/52538c08778c39a91ec2
