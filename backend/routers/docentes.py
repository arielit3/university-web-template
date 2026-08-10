from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import DocenteCreate, DocenteOut

# Definir el router
router = APIRouter(
    prefix="/docentes",
    tags=["docentes"]
)

@router.post("/", response_model=DocenteOut)
def crear_docente(docente: DocenteCreate, db: Session = Depends(get_db)):
    return crud.crear_docente(db, docente)

@router.get("/", response_model=list[DocenteOut])
def listar_docentes(db: Session = Depends(get_db)):
    return crud.listar_docentes(db)
