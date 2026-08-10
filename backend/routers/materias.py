from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import MateriaCreate, MateriaOut

# Definir el router
router = APIRouter(
    prefix="/materias",
    tags=["materias"]
)

@router.post("/", response_model=MateriaOut)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    return crud.crear_materia(db, materia)

@router.get("/", response_model=list[MateriaOut])
def listar_materias(db: Session = Depends(get_db)):
    return crud.listar_materias(db)
