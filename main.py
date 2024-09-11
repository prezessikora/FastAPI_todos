from os import name
from fastapi import FastAPI
import models
from database import engine
from routers import auth, health, todos
from starlette.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static",StaticFiles(directory='static'),name='static')

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(health.router)
