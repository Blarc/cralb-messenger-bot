from fastapi import FastAPI

from app.database import models
from app.database.database import engine
from app.routes import users, notes, messenger

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(messenger.router)
app.include_router(users.router)
app.include_router(notes.router)


@app.get('/')
def hello():
    return 'Hello, from Cralb!'
