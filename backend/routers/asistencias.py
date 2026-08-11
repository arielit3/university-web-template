from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import AsistenciaCreate, AsistenciaOut
from auth import solo_docente

# Definir el router
router = APIRouter(
    prefix="/asistencias",
    tags=["asistencias"]
)

@router.post("/", response_model=AsistenciaOut)
def registrar_asistencia(asistencia: AsistenciaCreate, usuario = Depends(solo_docente), db: Session = Depends(get_db)):
    asistencia_data = AsistenciaCreate(**{**asistencia.dict(), "idDocente": usuario.idUsuario})
    return crud.crear_asistencia(db, asistencia_data)

@router.get("/", response_model=list[AsistenciaOut])
def listar_asistencias(db: Session = Depends(get_db)):
    return crud.listar_asistencias(db)
