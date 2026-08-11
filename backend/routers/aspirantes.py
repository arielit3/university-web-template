from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import AspiranteCreate, AspiranteOut, AspiranteUpdate
from auth import obtener_usuario_actual, solo_admin

# Definir el router
router = APIRouter(
    prefix="/aspirantes",
    tags=["aspirantes"]
)


@router.post("/", response_model=AspiranteOut)
def crear_aspirante(aspirante: AspiranteCreate, usuario = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    if usuario.tipo not in ("director", "admin"):
        raise HTTPException(status_code=403, detail="No autorizado")

    if usuario.tipo == "director":
        carrera = crud.obtener_carrera_por_director(db, usuario.idUsuario)
        if not carrera:
            raise HTTPException(status_code=403, detail="Director sin carrera asignada")
        if aspirante.carreraSolicita.lower() != carrera.nombreCarrera.lower():
            raise HTTPException(status_code=403, detail="No puede crear aspirantes para otra carrera")

    return crud.crear_aspirante(db, aspirante)


@router.get("/", response_model=list[AspiranteOut])
def listar_aspirantes(usuario = Depends(solo_admin), db: Session = Depends(get_db)):
    return crud.listar_aspirantes(db)


@router.get("/me", response_model=AspiranteOut)
def obtener_mi_aspirante(usuario = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    if usuario.tipo != "aspirante":
        raise HTTPException(status_code=403, detail="Solo aspirantes pueden ver sus datos")
    aspirante = db.query(crud.Aspirante).filter(crud.Aspirante.idUsuario == usuario.idUsuario).first()
    if not aspirante:
        raise HTTPException(status_code=404, detail="Aspirante no encontrado")
    return aspirante


@router.get("/{idAspirante}", response_model=AspiranteOut)
def obtener_aspirante(idAspirante: int, usuario = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    aspirante = crud.obtener_aspirante_por_id(db, idAspirante)
    if not aspirante:
        raise HTTPException(status_code=404, detail="Aspirante no encontrado")
    if usuario.tipo == "aspirante":
        if aspirante.idUsuario != usuario.idUsuario:
            raise HTTPException(status_code=403, detail="No autorizado")
        return aspirante

    if usuario.tipo == "docente":
        carrera = crud.obtener_carrera_por_docente(db, usuario.idUsuario)
        if not carrera or aspirante.carreraSolicita.lower() != carrera.nombreCarrera.lower():
            raise HTTPException(status_code=403, detail="No autorizado")
        return aspirante

    if usuario.tipo == "director":
        carrera = crud.obtener_carrera_por_director(db, usuario.idUsuario)
        if not carrera or aspirante.carreraSolicita.lower() != carrera.nombreCarrera.lower():
            raise HTTPException(status_code=403, detail="No autorizado")
        return aspirante

    # admin puede ver cualquier aspirante
    return aspirante


@router.put("/{idAspirante}/puntos", response_model=AspiranteOut)
def actualizar_puntos(idAspirante: int, datos: AspiranteUpdate, usuario = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    if usuario.tipo not in ("director", "docente", "admin"):
        raise HTTPException(status_code=403, detail="No autorizado")

    aspirante = crud.obtener_aspirante_por_id(db, idAspirante)
    if not aspirante:
        raise HTTPException(status_code=404, detail="Aspirante no encontrado")

    if usuario.tipo == "docente":
        carrera = crud.obtener_carrera_por_docente(db, usuario.idUsuario)
        if not carrera or aspirante.carreraSolicita.lower() != carrera.nombreCarrera.lower():
            raise HTTPException(status_code=403, detail="No autorizado")

    if usuario.tipo == "director":
        carrera = crud.obtener_carrera_por_director(db, usuario.idUsuario)
        if not carrera or aspirante.carreraSolicita.lower() != carrera.nombreCarrera.lower():
            raise HTTPException(status_code=403, detail="No autorizado")

    aspirante = crud.actualizar_puntos_aspirante(db, idAspirante, datos.puntosExamen)
    return aspirante
