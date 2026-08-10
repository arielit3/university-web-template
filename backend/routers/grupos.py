from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import GrupoCreate, GrupoOut

# Definir el router
router = APIRouter(
    prefix="/grupos",
    tags=["grupos"]
)

@router.post("/", response_model=GrupoOut)
def crear_grupo(grupo: GrupoCreate, db: Session = Depends(get_db)):
    return crud.crear_grupo(db, grupo)

@router.get("/", response_model=list[GrupoOut])
def listar_grupos(db: Session = Depends(get_db)):
    return crud.listar_grupos(db)
