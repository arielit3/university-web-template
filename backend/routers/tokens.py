from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import TokenCreate, TokenOut
from auth import solo_admin

# Definir el router
router = APIRouter(
    prefix="/tokens",
    tags=["tokens"]
)

@router.post("/", response_model=TokenOut)
def crear_token(token: TokenCreate, usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.crear_token(db, token)

@router.get("/", response_model=list[TokenOut])
def listar_tokens(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_tokens(db)
