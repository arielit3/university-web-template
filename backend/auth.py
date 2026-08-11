from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import crud
from models import Usuario

SECRET_KEY = "supersecretkey"  # cámbialo por algo seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- Funciones de seguridad ---
def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def crear_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("idUsuario")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = crud.obtener_usuario_por_id(db, user_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# --- Dependencias de roles ---
def solo_director(usuario: Usuario = Depends(obtener_usuario_actual)):
    if usuario.tipo != "director":
        raise HTTPException(status_code=403, detail="No autorizado")
    return usuario

def solo_docente(usuario: Usuario = Depends(obtener_usuario_actual)):
    if usuario.tipo != "docente":
        raise HTTPException(status_code=403, detail="No autorizado")
    return usuario

def solo_alumno(usuario: Usuario = Depends(obtener_usuario_actual)):
    if usuario.tipo != "alumno":
        raise HTTPException(status_code=403, detail="No autorizado")
    return usuario
def solo_admin(usuario: Usuario = Depends(obtener_usuario_actual)):
    if usuario.tipo != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    return usuario
