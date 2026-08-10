from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import AsistenciaCreate, AsistenciaOut

# Definir el router
router = APIRouter(
    prefix="/asistencias",
    tags=["asistencias"]
)

@router.post("/", response_model=AsistenciaOut)
def registrar_asistencia(asistencia: AsistenciaCreate, db: Session = Depends(get_db)):
    return crud.crear_asistencia(db, asistencia)

@router.get("/", response_model=list[AsistenciaOut])
def listar_asistencias(db: Session = Depends(get_db)):
    return crud.listar_asistencias(db)
