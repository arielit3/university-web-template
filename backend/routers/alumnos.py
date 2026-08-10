from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import AlumnoCreate, AlumnoOut

# Definir el router
router = APIRouter(
    prefix="/alumnos",
    tags=["alumnos"]
)

@router.post("/", response_model=AlumnoOut)
def crear_alumno(alumno: AlumnoCreate, db: Session = Depends(get_db)):
    return crud.crear_alumno(db, alumno)

@router.get("/", response_model=list[AlumnoOut])
def listar_alumnos(db: Session = Depends(get_db)):
    return crud.listar_alumnos(db)
