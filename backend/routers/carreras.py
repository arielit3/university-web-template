from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import CarreraCreate, CarreraOut
from auth import solo_admin

# Definir el router
router = APIRouter(
    prefix="/carreras",
    tags=["carreras"]
)

@router.post("/", response_model=CarreraOut)
def crear_carrera(carrera: CarreraCreate, usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.crear_carrera(db, carrera)

@router.get("/", response_model=list[CarreraOut])
def listar_carreras(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_carreras(db)
