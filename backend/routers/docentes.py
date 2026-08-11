from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import DocenteCreate, DocenteOut, CalificacionCreate, AsistenciaCreate
from auth import solo_docente, solo_director, solo_admin

# Definir el router
router = APIRouter(
    prefix="/docentes",
    tags=["docentes"]
)

@router.post("/", response_model=DocenteOut)
def crear_docente(docente: DocenteCreate, usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.crear_docente(db, docente)

@router.get("/", response_model=list[DocenteOut])
def listar_docentes(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_docentes(db)

# --- Docente: ver sus grupos ---
@router.get("/mis-grupos")
def mis_grupos(usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    return crud.listar_grupos_por_docente(db, usuario.idUsuario)

# --- Docente: ver alumnos de sus grupos ---
@router.get("/mis-alumnos")
def mis_alumnos(usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    return crud.listar_alumnos_por_grupos_docente(db, usuario.idUsuario)

# --- Docente: listar materias que imparte ---
@router.get("/mis-materias")
def mis_materias(usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    return crud.listar_materias_por_docente(db, usuario.idUsuario)

# --- Docente: registrar calificación ---
@router.post("/registrar-calificacion")
def registrar_calificacion(calificacion: CalificacionCreate, usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    return crud.registrar_calificacion(db, usuario.idUsuario, calificacion)

# --- Docente: registrar asistencia ---
@router.post("/registrar-asistencia")
def registrar_asistencia(asistencia: AsistenciaCreate, usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    return crud.registrar_asistencia(db, usuario.idUsuario, asistencia)

# --- Docente: listar asistencias de sus grupos ---
@router.get("/mis-asistencias")
def mis_asistencias(usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    return crud.listar_asistencias_por_docente(db, usuario.idUsuario)

