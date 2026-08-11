from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import crear_token, verificar_password
import crud
from schemas import UsuarioLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = crud.obtener_usuario_por_correo(db, datos.correo)
    if not usuario or not verificar_password(datos.contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token({
        "idUsuario": usuario.idUsuario,
        "tipo": usuario.tipo,
        "idCarrera": getattr(usuario, "idCarrera", None)
    })
    return {"access_token": token, "token_type": "bearer"}
