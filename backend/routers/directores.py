from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import solo_director
import crud
from schemas import AspiranteCreate, DocenteCreate

from fastapi import Query
from schemas import RegistrarAspiranteRequest, UsuarioCreate, AspiranteCreate
from auth import hash_password

router = APIRouter(prefix="/directores", tags=["directores"])


def obtener_carrera_director(usuario, db: Session):
    carrera = crud.obtener_carrera_por_director(db, usuario.idUsuario)
    if not carrera:
        raise HTTPException(status_code=403, detail="Director sin carrera asignada")
    return carrera


@router.get("/mi-carrera")
def mi_carrera(usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    return carrera


# --- Director: buscar usuario por correo (para llenar idUsuario al crear aspirante)
@router.get("/buscar-usuario")
def buscar_usuario(correo: str = Query(..., min_length=3), usuario = Depends(solo_director), db: Session = Depends(get_db)):
    u = crud.obtener_usuario_por_correo(db, correo)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # devolver solo campos necesarios
    return {"idUsuario": u.idUsuario, "nombre": u.nombre, "apellido": u.apellido, "correo": u.correo}


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


# --- Director: registrar aspirante (crea usuario tipo 'aspirante' si no existe)
@router.post("/registrar-aspirante")
def registrar_aspirante(payload: RegistrarAspiranteRequest, usuario = Depends(solo_director), db: Session = Depends(get_db)):
    carrera = obtener_carrera_director(usuario, db)
    if payload.carreraSolicita.lower() != carrera.nombreCarrera.lower():
        raise HTTPException(status_code=403, detail="No puede crear aspirantes para otra carrera")

    # Si se proporciona idUsuario, crear solo el registro de aspirante
    if payload.idUsuario:
        u = crud.obtener_usuario_por_id(db, payload.idUsuario)
        if not u:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        # asegurar que el usuario sea tipo aspirante
        if u.tipo != 'aspirante':
            u.tipo = 'aspirante'
            db.add(u)
            db.commit()
            db.refresh(u)
        aspirante = crud.crear_aspirante(db, AspiranteCreate(
            idUsuario=payload.idUsuario,
            numFicha=payload.numFicha,
            periodo=payload.periodo,
            carreraSolicita=payload.carreraSolicita,
            puntosExamen=payload.puntosExamen or 0
        ))
        return aspirante

    # Crear nuevo usuario + aspirante
    # validar campos
    if not (payload.nombre and payload.apellido and payload.correo and payload.contraseña):
        raise HTTPException(status_code=400, detail="Faltan datos para crear el usuario aspirante")
    # verificar correo no existente
    if crud.obtener_usuario_por_correo(db, payload.correo):
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    hashed = hash_password(payload.contraseña)
    nuevo = crud.crear_usuario(db, UsuarioCreate(
        nombre=payload.nombre,
        apellido=payload.apellido,
        correo=payload.correo,
        contraseña=hashed,
        tipo='aspirante'
    ))
    aspirante = crud.crear_aspirante(db, AspiranteCreate(
        idUsuario=nuevo.idUsuario,
        numFicha=payload.numFicha,
        periodo=payload.periodo,
        carreraSolicita=payload.carreraSolicita,
        puntosExamen=payload.puntosExamen or 0
    ))
    return { 'usuario': { 'idUsuario': nuevo.idUsuario, 'correo': nuevo.correo }, 'aspirante': aspirante }
