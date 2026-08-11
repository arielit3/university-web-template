from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import CalificacionCreate, CalificacionOut
from auth import solo_admin, solo_docente

# Definir el router
router = APIRouter(
    prefix="/calificaciones",
    tags=["calificaciones"]
)

@router.post("/", response_model=CalificacionOut)
def crear_calificacion(calificacion: CalificacionCreate, usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    # For security, force the idDocente to the logged-in docente
    cal_data = CalificacionCreate(**{**calificacion.dict(), "idDocente": usuario.idUsuario})
    return crud.crear_calificacion(db, cal_data)

@router.get("/", response_model=list[CalificacionOut])
def listar_calificaciones(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_calificaciones(db)
