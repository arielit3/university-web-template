from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from auth import crear_token, verificar_password, obtener_usuario_actual
import crud
from schemas import UsuarioOut
import urllib.parse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    """Accept either JSON body with keys `correo`/`contraseña` or OAuth2 password form-data
    so Swagger's "Authorize" (password flow) works and frontend JSON requests also work.
    """
    content_type = (request.headers.get("content-type") or "").lower()
    correo = None
    contraseña = None

    if content_type.startswith("application/json"):
        data = await request.json()
        correo = data.get("correo")
        contraseña = data.get("contraseña")
    else:
        # handle application/x-www-form-urlencoded without requiring python-multipart
        if content_type.startswith("application/x-www-form-urlencoded"):
            body = await request.body()
            try:
                parsed = urllib.parse.parse_qs(body.decode())
            except Exception:
                parsed = {}
            correo_list = parsed.get("username") or parsed.get("correo")
            contraseña_list = parsed.get("password") or parsed.get("contraseña")
            correo = correo_list[0] if isinstance(correo_list, list) and correo_list else (correo_list if isinstance(correo_list, str) else None)
            contraseña = contraseña_list[0] if isinstance(contraseña_list, list) and contraseña_list else (contraseña_list if isinstance(contraseña_list, str) else None)
        else:
            try:
                form = await request.form()
            except AssertionError:
                raise HTTPException(status_code=500, detail="Form parsing requires 'python-multipart'. Install it in the backend venv: pip install python-multipart")
            # Swagger/OAuth2 password field names are 'username' and 'password'
            correo = form.get("username") or form.get("correo")
            contraseña = form.get("password") or form.get("contraseña")

    if not correo or not contraseña:
        raise HTTPException(status_code=422, detail="Faltan credenciales")

    usuario = crud.obtener_usuario_por_correo(db, correo)
    if not usuario or not verificar_password(contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token({
        "idUsuario": usuario.idUsuario,
        "tipo": usuario.tipo,
        "idCarrera": getattr(usuario, "idCarrera", None)
    })
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioOut)
def me(usuario = Depends(obtener_usuario_actual)):
    return usuario


@router.post("/logout")
def logout(usuario = Depends(obtener_usuario_actual)):
    # No server-side token revocation implemented; client should remove token.
    return {"msg": "Cierre de sesión exitoso"}
