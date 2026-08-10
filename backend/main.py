from fastapi import FastAPI
from database import Base, engine
import models
app = FastAPI()


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"mensaje": "Hola USN"}   