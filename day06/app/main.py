from fastapi import FastAPI
from .database import database
from .routers.students import router

app = FastAPI()

app.include_router(router)
