from fastapi import FastAPI

from app.api import router


app = FastAPI(title="FruitAPI")
app.include_router(router)

