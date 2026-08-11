from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import MateriaCreate, MateriaOut
from auth import solo_director

# Definir el router
router = APIRouter(
    prefix="/materias",
    tags=["materias"]
)

@router.post("/", response_model=MateriaOut)
def crear_materia(materia: MateriaCreate, usuario = Depends(solo_director), db: Session = Depends(get_db)):
    return crud.crear_materia(db, materia)

from auth import solo_admin

@router.get("/", response_model=list[MateriaOut])
def listar_materias(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_materias(db)
