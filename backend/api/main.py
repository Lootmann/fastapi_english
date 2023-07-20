from fastapi import FastAPI

from api.routers.examples import router as example_router
from api.routers.words import router as word_router

app = FastAPI()

app.include_router(word_router)
app.include_router(example_router)
