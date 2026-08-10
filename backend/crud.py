from sqlalchemy.orm import Session
from models import Usuario, Aspirante
from schemas import UsuarioCreate, AspiranteCreate

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

def listar_usuarios(db: Session):
    return db.query(Usuario).all()


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

def listar_aspirantes(db: Session):
    return db.query(Aspirante).all()



from models import Alumno
from schemas import AlumnoCreate

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

def listar_alumnos(db: Session):
    return db.query(Alumno).all()



from models import Docente
from schemas import DocenteCreate

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

from models import Carrera
from schemas import CarreraCreate

def crear_carrera(db: Session, carrera: CarreraCreate):
    nueva = Carrera(
        nombreCarrera=carrera.nombreCarrera,
        planEstudios=carrera.planEstudios
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_carreras(db: Session):
    return db.query(Carrera).all()

from models import Grupo
from schemas import GrupoCreate

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

from models import Materia
from schemas import MateriaCreate

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

from models import GrupoMateria
from schemas import GrupoMateriaCreate

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

from models import Calificacion
from schemas import CalificacionCreate

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
from models import Asistencia
from schemas import AsistenciaCreate

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
from models import Token
from schemas import TokenCreate
from datetime import datetime

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


from models import Director
from schemas import DirectorCreate

def crear_director(db: Session, director: DirectorCreate):
    nuevo = Director(
        idUsuario=director.idUsuario,
        idCarrera=director.idCarrera
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
