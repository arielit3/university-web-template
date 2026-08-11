from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import (
    Usuario, Aspirante, Alumno, Docente, Carrera, Grupo,
    Materia, GrupoMateria, Calificacion, Asistencia, Token
)
from schemas import (
    UsuarioCreate, AspiranteCreate, AlumnoCreate, DocenteCreate,
    CarreraCreate, GrupoCreate, MateriaCreate, GrupoMateriaCreate,
    CalificacionCreate, AsistenciaCreate, TokenCreate
)

# --- Usuarios ---
def crear_usuario(db: Session, usuario: UsuarioCreate):
    nuevo = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        contraseña=usuario.contraseña,
        tipo=usuario.tipo
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_usuarios(db: Session) -> List[Usuario]:
    return db.query(Usuario).all()

def obtener_usuario_por_id(db: Session, idUsuario: int):
    return db.query(Usuario).filter(Usuario.idUsuario == idUsuario).first()

def obtener_usuario_por_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()


def obtener_carrera_por_director(db: Session, idDirector: int):
    return db.query(Carrera).filter(Carrera.idDirector == idDirector).first()


def obtener_docente_por_usuario(db: Session, idUsuario: int):
    return db.query(Docente).filter(Docente.idUsuario == idUsuario).first()


def obtener_carrera_por_docente(db: Session, idUsuario: int):
    docente = obtener_docente_por_usuario(db, idUsuario)
    if not docente:
        return None
    return db.query(Carrera).filter(Carrera.idCarrera == docente.idCarrera).first()


# --- Aspirantes ---
def crear_aspirante(db: Session, aspirante: AspiranteCreate):
    nuevo = Aspirante(
        idUsuario=aspirante.idUsuario,
        numFicha=aspirante.numFicha,
        periodo=aspirante.periodo,
        carreraSolicita=aspirante.carreraSolicita,
        puntosExamen=aspirante.puntosExamen
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_aspirantes(db: Session) -> List[Aspirante]:
    return db.query(Aspirante).all()

def obtener_aspirante_por_id(db: Session, idAspirante: int):
    return db.query(Aspirante).filter(Aspirante.idAspirante == idAspirante).first()

def actualizar_puntos_aspirante(db: Session, idAspirante: int, puntos: int):
    aspirante = obtener_aspirante_por_id(db, idAspirante)
    if not aspirante:
        return None
    aspirante.puntosExamen = puntos
    db.add(aspirante)
    db.commit()
    db.refresh(aspirante)
    return aspirante

def promover_aspirante_a_alumno(db: Session, aspirante: Aspirante):
    promedio = float(aspirante.puntosExamen or 0)
    alumno = Alumno(
        idUsuario=aspirante.idUsuario,
        idGrupo=None,
        promedioPrep=int(promedio)
    )
    db.add(alumno)
    db.delete(aspirante)
    db.commit()
    db.refresh(alumno)
    return alumno


# --- Alumnos ---
def crear_alumno(db: Session, alumno: AlumnoCreate):
    nuevo = Alumno(
        idUsuario=alumno.idUsuario,
        idGrupo=alumno.idGrupo,
        promedioPrep=alumno.promedioPrep
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_alumnos(db: Session) -> List[Alumno]:
    return db.query(Alumno).all()

def listar_alumnos_por_carrera(db: Session, idCarrera: int):
    return (
        db.query(Alumno)
        .join(Grupo, Alumno.idGrupo == Grupo.idGrupo)
        .filter(Grupo.idCarrera == idCarrera)
        .all()
    )

def listar_alumnos_por_grupos_docente(db: Session, idUsuario: int):
    grupos = db.query(Grupo).filter(Grupo.idDocente == idUsuario).all()
    ids_grupos = [g.idGrupo for g in grupos]
    if not ids_grupos:
        return []
    return db.query(Alumno).filter(Alumno.idGrupo.in_(ids_grupos)).all()


# --- Grupos / Materias / Materia-asignacion ---
def crear_docente(db: Session, docente: DocenteCreate):
    nuevo = Docente(
        idUsuario=docente.idUsuario,
        idCarrera=docente.idCarrera,
        nivelEstudios=docente.nivelEstudios,
        turno=docente.turno
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_docentes(db: Session):
    return db.query(Docente).all()

def listar_docentes_por_carrera(db: Session, idCarrera: int):
    return db.query(Docente).filter(Docente.idCarrera == idCarrera).all()

def crear_carrera(db: Session, carrera: CarreraCreate):
    nueva = Carrera(
        nombreCarrera=carrera.nombreCarrera,
        planEstudios=carrera.planEstudios,
        idDirector=carrera.idDirector
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_carreras(db: Session):
    return db.query(Carrera).all()

def crear_grupo(db: Session, grupo: GrupoCreate):
    nuevo = Grupo(
        idCarrera=grupo.idCarrera,
        idDocente=grupo.idDocente,
        nombreGrupo=grupo.nombreGrupo,
        periodo=grupo.periodo,
        numAlumnos=grupo.numAlumnos
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_grupos(db: Session):
    return db.query(Grupo).all()

def listar_grupos_por_docente(db: Session, idUsuario: int):
    return db.query(Grupo).filter(Grupo.idDocente == idUsuario).all()

def crear_materia(db: Session, materia: MateriaCreate):
    nueva = Materia(
        nombreMateria=materia.nombreMateria,
        unidades=materia.unidades,
        objetivo=materia.objetivo,
        idCarrera=materia.idCarrera
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_materias(db: Session):
    return db.query(Materia).all()

def listar_materias_por_carrera(db: Session, idCarrera: int):
    return db.query(Materia).filter(Materia.idCarrera == idCarrera).all()

def listar_materias_por_docente(db: Session, idUsuario: int):
    grupos = db.query(Grupo).filter(Grupo.idDocente == idUsuario).all()
    ids_grupos = [g.idGrupo for g in grupos]
    if not ids_grupos:
        return []
    return (
        db.query(Materia)
        .join(GrupoMateria, GrupoMateria.idMateria == Materia.idMateria)
        .filter(GrupoMateria.idGrupo.in_(ids_grupos))
        .all()
    )

def listar_materias_por_alumno(db: Session, idUsuario: int):
    alumno = db.query(Alumno).filter(Alumno.idUsuario == idUsuario).first()
    if alumno and alumno.idGrupo:
        return (
            db.query(Materia)
            .join(GrupoMateria, GrupoMateria.idMateria == Materia.idMateria)
            .filter(GrupoMateria.idGrupo == alumno.idGrupo)
            .all()
        )
    return []

def crear_grupo_materia(db: Session, asignacion: GrupoMateriaCreate):
    nueva = GrupoMateria(
        idGrupo=asignacion.idGrupo,
        idMateria=asignacion.idMateria
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_grupo_materia(db: Session):
    return db.query(GrupoMateria).all()


# --- Calificaciones / Asistencias ---
def crear_calificacion(db: Session, calificacion: CalificacionCreate):
    nueva = Calificacion(
        idAlumno=calificacion.idAlumno,
        idMateria=calificacion.idMateria,
        idDocente=calificacion.idDocente,
        calUnidad1=calificacion.calUnidad1,
        calUnidad2=calificacion.calUnidad2,
        calUnidad3=calificacion.calUnidad3
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_calificaciones(db: Session):
    return db.query(Calificacion).all()

def listar_calificaciones_por_alumno(db: Session, idUsuario: int):
    alumno = db.query(Alumno).filter(Alumno.idUsuario == idUsuario).first()
    if alumno:
        return db.query(Calificacion).filter(Calificacion.idAlumno == alumno.idAlumno).all()
    return []

def crear_asistencia(db: Session, asistencia: AsistenciaCreate):
    nueva = Asistencia(
        idAlumno=asistencia.idAlumno,
        idMateria=asistencia.idMateria,
        idDocente=asistencia.idDocente,
        fecha=asistencia.fecha,
        asistencia=asistencia.asistencia
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_asistencias(db: Session):
    return db.query(Asistencia).all()

def listar_asistencias_por_docente(db: Session, idUsuario: int):
    return db.query(Asistencia).join(Alumno, Asistencia.idAlumno == Alumno.idAlumno).join(Grupo, Alumno.idGrupo == Grupo.idGrupo).filter(Grupo.idDocente == idUsuario).all()

def listar_asistencias_por_alumno(db: Session, idUsuario: int):
    alumno = db.query(Alumno).filter(Alumno.idUsuario == idUsuario).first()
    if alumno:
        return db.query(Asistencia).filter(Asistencia.idAlumno == alumno.idAlumno).all()
    return []


# --- Tokens ---
def crear_token(db: Session, token: TokenCreate):
    nuevo = Token(
        idUsuario=token.idUsuario,
        token=token.token,
        fechaGeneracion=datetime.now(),
        fechaExpiracion=token.fechaExpiracion,
        utilizado=token.utilizado
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_tokens(db: Session):
    return db.query(Token).all()
