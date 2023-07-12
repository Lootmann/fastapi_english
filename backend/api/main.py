from fastapi import FastAPI

from api.routers.words import router as word_router

app = FastAPI()

app.include_router(word_router)
