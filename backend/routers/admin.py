from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import solo_admin
import crud

router = APIRouter(prefix="/admin", tags=["admin"])

# --- Admin: listar todos los usuarios ---
@router.get("/usuarios")
def listar_todos_usuarios(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_usuarios(db)

# --- Admin: listar todas las carreras ---
@router.get("/carreras")
def listar_todas_carreras(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_carreras(db)

# --- Admin: listar todas las materias ---
@router.get("/materias")
def listar_todas_materias(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_materias(db)

# --- Admin: listar todos los grupos ---
@router.get("/grupos")
def listar_todos_grupos(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_grupos(db)

# --- Admin: listar todas las calificaciones ---
@router.get("/calificaciones")
def listar_todas_calificaciones(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_calificaciones(db)

# --- Admin: listar todas las asistencias ---
@router.get("/asistencias")
def listar_todas_asistencias(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_asistencias(db)
