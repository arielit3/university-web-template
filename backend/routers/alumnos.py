from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import AlumnoCreate, AlumnoOut
from auth import solo_admin, solo_alumno

# Definir el router
router = APIRouter(
    prefix="/alumnos",
    tags=["alumnos"]
)

@router.post("/", response_model=AlumnoOut)
def crear_alumno(alumno: AlumnoCreate, usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.crear_alumno(db, alumno)

@router.get("/", response_model=list[AlumnoOut])
def listar_alumnos(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_alumnos(db)

# --- Alumno: ver sus calificaciones ---
@router.get("/mis-calificaciones")
def mis_calificaciones(usuario = Depends(solo_alumno), db: Session = Depends(get_db)):
    return crud.listar_calificaciones_por_alumno(db, usuario.idUsuario)

# --- Alumno: ver sus asistencias ---
@router.get("/mis-asistencias")
def mis_asistencias(usuario = Depends(solo_alumno), db: Session = Depends(get_db)):
    return crud.listar_asistencias_por_alumno(db, usuario.idUsuario)

# --- Alumno: listar materias de su grupo ---
@router.get("/mis-materias")
def mis_materias(usuario = Depends(solo_alumno), db: Session = Depends(get_db)):
    return crud.listar_materias_por_alumno(db, usuario.idUsuario)

