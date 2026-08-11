from fastapi import FastAPI
from database import Base, engine
import models
from routers import auth, admin, directores, usuarios, aspirantes
from routers import alumnos, docentes, carreras, grupos
from routers import materias, grupo_materia, calificaciones, asistencias
from routers import tokens, seed

app = FastAPI()


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"mensaje": "Hola USN"}

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(directores.router)
app.include_router(usuarios.router)
app.include_router(aspirantes.router)
app.include_router(alumnos.router)
app.include_router(docentes.router)
app.include_router(carreras.router)
app.include_router(grupos.router)
app.include_router(materias.router)
app.include_router(grupo_materia.router)
app.include_router(calificaciones.router)
app.include_router(asistencias.router)
app.include_router(tokens.router)
app.include_router(seed.router)
