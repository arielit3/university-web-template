from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import solo_director
import crud
from schemas import AspiranteCreate, DocenteCreate

router = APIRouter(prefix="/directores", tags=["directores"])


def obtener_carrera_director(usuario, db: Session):
    carrera = crud.obtener_carrera_por_director(db, usuario.idUsuario)
    if not carrera:
        raise HTTPException(status_code=403, detail="Director sin carrera asignada")
    return carrera


# --- Director: listar alumnos de su carrera ---
@router.get("/alumnos")
def alumnos_de_mi_carrera(usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    return crud.listar_alumnos_por_carrera(db, carrera.idCarrera)


# --- Director: listar docentes de su carrera ---
@router.get("/docentes")
def docentes_de_mi_carrera(usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    return crud.listar_docentes_por_carrera(db, carrera.idCarrera)


# --- Director: listar materias de su carrera ---
@router.get("/materias")
def materias_de_mi_carrera(usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    return crud.listar_materias_por_carrera(db, carrera.idCarrera)


# --- Director: listar grupos de su carrera ---
@router.get("/grupos")
def grupos_de_mi_carrera(usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    return crud.listar_grupos_por_carrera(db, carrera.idCarrera)


# --- Director: crear aspirante ---
@router.post("/crear-aspirante")
def crear_aspirante(aspirante: AspiranteCreate, usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    if aspirante.carreraSolicita.lower() != carrera.nombreCarrera.lower():
        raise HTTPException(status_code=403, detail="No puede crear aspirantes para otra carrera")
    return crud.crear_aspirante(db, aspirante)


# --- Director: crear docente ---
@router.post("/crear-docente")
def crear_docente(docente: DocenteCreate, usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    if docente.idCarrera != carrera.idCarrera:
        raise HTTPException(status_code=403, detail="No puede crear docentes para otra carrera")
    return crud.crear_docente(db, docente)


# --- Director: promover aspirante a alumno ---
@router.put("/promover-aspirante/{idAspirante}")
def promover_aspirante(idAspirante: int, usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    aspirante = crud.obtener_aspirante_por_id(db, idAspirante)
    if not aspirante:
        raise HTTPException(status_code=404, detail="Aspirante no encontrado")
    if aspirante.carreraSolicita.lower() != carrera.nombreCarrera.lower():
        raise HTTPException(status_code=403, detail="No puede promover aspirantes de otra carrera")
    if (aspirante.puntosExamen or 0) < 90:
        raise HTTPException(status_code=400, detail="El aspirante no cumple con el requisito")
    return crud.promover_aspirante_a_alumno(db, aspirante)
