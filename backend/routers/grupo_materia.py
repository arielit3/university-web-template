from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import GrupoMateriaCreate, GrupoMateriaOut

# Definir el router
router = APIRouter(
    prefix="/grupo-materia",
    tags=["grupo-materia"]
)

@router.post("/", response_model=GrupoMateriaOut)
def asignar_materia_a_grupo(asignacion: GrupoMateriaCreate, db: Session = Depends(get_db)):
    return crud.crear_grupo_materia(db, asignacion)

@router.get("/", response_model=list[GrupoMateriaOut])
def listar_asignaciones(db: Session = Depends(get_db)):
    return crud.listar_grupo_materia(db)
