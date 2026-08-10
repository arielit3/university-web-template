from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import CalificacionCreate, CalificacionOut

# Definir el router
router = APIRouter(
    prefix="/calificaciones",
    tags=["calificaciones"]
)

@router.post("/", response_model=CalificacionOut)
def crear_calificacion(calificacion: CalificacionCreate, db: Session = Depends(get_db)):
    return crud.crear_calificacion(db, calificacion)

@router.get("/", response_model=list[CalificacionOut])
def listar_calificaciones(db: Session = Depends(get_db)):
    return crud.listar_calificaciones(db)
