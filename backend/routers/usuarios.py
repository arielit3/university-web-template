from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import UsuarioCreate, UsuarioOut

# Definir el router
router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.post("/", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_usuario(db, usuario)

@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.listar_usuarios(db)

from auth import solo_director, solo_docente, solo_alumno

# Solo directores pueden listar alumnos de su carrera
@router.get("/alumnos")
def listar_alumnos_director(usuario = Depends(solo_director), db: Session = Depends(get_db)):
    return crud.listar_alumnos_por_carrera(db, usuario.idCarrera)

# Solo docentes pueden listar alumnos de sus grupos
@router.get("/mis-alumnos")
def listar_alumnos_docente(usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    return crud.listar_alumnos_por_grupos_docente(db, usuario.idUsuario)

# Solo alumnos pueden ver sus calificaciones
@router.get("/mis-calificaciones")
def mis_calificaciones(usuario = Depends(solo_alumno), db: Session = Depends(get_db)):
    return crud.listar_calificaciones_por_alumno(db, usuario.idUsuario)

