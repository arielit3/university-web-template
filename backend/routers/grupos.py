from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import GrupoCreate, GrupoOut
from auth import solo_director, solo_admin

# Definir el router
router = APIRouter(
    prefix="/grupos",
    tags=["grupos"]
)

@router.post("/", response_model=GrupoOut)
def crear_grupo(grupo: GrupoCreate, usuario = Depends(solo_director), db: Session = Depends(get_db)):
    return crud.crear_grupo(db, grupo)

from auth import solo_admin

@router.get("/", response_model=list[GrupoOut])
def listar_grupos(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_grupos(db)
