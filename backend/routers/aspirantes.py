from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import AspiranteCreate, AspiranteOut

# Definir el router
router = APIRouter(
    prefix="/aspirantes",
    tags=["aspirantes"]
)

@router.post("/", response_model=AspiranteOut)
def crear_aspirante(aspirante: AspiranteCreate, db: Session = Depends(get_db)):
    return crud.crear_aspirante(db, aspirante)

@router.get("/", response_model=list[AspiranteOut])
def listar_aspirantes(db: Session = Depends(get_db)):
    return crud.listar_aspirantes(db)
