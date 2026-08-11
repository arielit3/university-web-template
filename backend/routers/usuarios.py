from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import UsuarioCreate, UsuarioOut
from auth import solo_admin, solo_director, solo_docente, solo_alumno

# Definir el router
router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.post("/", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, usuario_actual = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.crear_usuario(db, usuario)

@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(usuario_actual = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_usuarios(db)

# Solo directores pueden listar alumnos de su carrera
@router.get("/alumnos")
def listar_alumnos_director(usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = crud.obtener_carrera_por_director(db, usuario.idUsuario)
    if not carrera:
        raise HTTPException(status_code=403, detail="Director sin carrera asignada")
    return crud.listar_alumnos_por_carrera(db, carrera.idCarrera)

# Solo docentes pueden listar alumnos de sus grupos
@router.get("/mis-alumnos")
def listar_alumnos_docente(usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    return crud.listar_alumnos_por_grupos_docente(db, usuario.idUsuario)

# Solo alumnos pueden ver sus calificaciones
@router.get("/mis-calificaciones")
def mis_calificaciones(usuario = Depends(solo_alumno), db: Session = Depends(get_db)):
    return crud.listar_calificaciones_por_alumno(db, usuario.idUsuario)

