from fastapi import FastAPI
from database import Base, engine
import models
from routers import usuarios, aspirantes
from routers import alumnos
from routers import docentes

app = FastAPI()



Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"mensaje": "Hola USN"}   

app.include_router(usuarios.router)
app.include_router(aspirantes.router)
app.include_router(alumnos.router)

app.include_router(docentes.router)

from routers import carreras
app.include_router(carreras.router)
from routers import grupos
app.include_router(grupos.router)
from routers import materias
app.include_router(materias.router)
from routers import grupo_materia
app.include_router(grupo_materia.router)
