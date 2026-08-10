from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    idUsuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    contraseña = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # aspirante, alumno, docente, director
    fechaRegistro = Column(DateTime, default=datetime.datetime.utcnow)
    activo = Column(Boolean, default=True)

    # Relaciones con otras tablas
    aspirante = relationship("Aspirante", back_populates="usuario", uselist=False)
    alumno = relationship("Alumno", back_populates="usuario", uselist=False)
    docente = relationship("Docente", back_populates="usuario", uselist=False)
    # Si es director, opcionalmente puede tener una carrera asignada, asi sabremos que es 
    # director de esa carrera
    idCarrera = Column(Integer, ForeignKey("carreras.idCarrera"), nullable=True)

class Aspirante(Base):
    __tablename__ = "aspirantes"

    idAspirante = Column(Integer, primary_key=True, index=True)
    idUsuario = Column(Integer, ForeignKey("usuarios.idUsuario"))
    numFicha = Column(Integer, unique=True, nullable=False)  
    periodo = Column(String, nullable=False) 
    carreraSolicita = Column(String, nullable=False)
    puntosExamen = Column(Integer, nullable=True)

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="aspirante")

class Alumno(Base):
    __tablename__ = "alumnos"

    idAlumno = Column(Integer, primary_key=True, index=True)
    idUsuario = Column(Integer, ForeignKey("usuarios.idUsuario"))
    idGrupo = Column(Integer, ForeignKey("grupos.idGrupo"), nullable=True)
    fechaIngreso = Column(DateTime, default=datetime.datetime.utcnow)
    promedioPrep = Column(Integer, nullable=False)  # promedio con el que ingres

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="alumno")
    # Relación con Grupo
    grupo = relationship("Grupo", back_populates="alumnos")
    calificaciones = relationship("Calificacion", back_populates="alumno")
    asistencias = relationship("Asistencia", back_populates="alumno")


class Docente(Base):
    __tablename__ = "docentes"

    idDocente = Column(Integer, primary_key=True, index=True)
    idUsuario = Column(Integer, ForeignKey("usuarios.idUsuario"))
    idCarrera = Column(Integer, ForeignKey("carreras.idCarrera"))
    fechaIngreso = Column(DateTime, default=datetime.datetime.utcnow)
    nivelEstudios = Column(String, nullable=False)  
    turno = Column(String, nullable=False) 

    usuario = relationship("Usuario", back_populates="docente")
    carrera = relationship("Carrera", back_populates="docentes")
    grupos = relationship("Grupo", back_populates="docente")

class Carrera(Base):
    __tablename__ = "carreras"

    idCarrera = Column(Integer, primary_key=True, index=True)
    nombreCarrera = Column(String, unique=True, nullable=False)
    planEstudios = Column(Integer, nullable=False)  # número de semestres/cuatrimestres

    # Relación con Docentes
    docentes = relationship("Docente", back_populates="carrera")
    # Relación con Grupos
    grupos = relationship("Grupo", back_populates="carrera")
    # Relación con Materias
    materias = relationship("Materia", back_populates="carrera")


class Grupo(Base):
    __tablename__ = "grupos"

    idGrupo = Column(Integer, primary_key=True, index=True)
    idCarrera = Column(Integer, ForeignKey("carreras.idCarrera"))
    idDocente = Column(Integer, ForeignKey("docentes.idDocente"))
    nombreGrupo = Column(String, nullable=False)  # ej. "IS-101"
    periodo = Column(String, nullable=False)      # ej. "Agosto-Diciembre 2026"
    numAlumnos = Column(Integer, default=0)       # contador de alumnos asignados

    # Relación con Carrera
    carrera = relationship("Carrera", back_populates="grupos")
    # Relación con Docente
    docente = relationship("Docente", back_populates="grupos")
    # Relación con Alumnos
    alumnos = relationship("Alumno", back_populates="grupo")
    # Relación con Materias (tabla intermedia después)
    materias = relationship("GrupoMateria", back_populates="grupo")

    

class Materia(Base):
    __tablename__ = "materias"

    idMateria = Column(Integer, primary_key=True, index=True)
    nombreMateria = Column(String, nullable=False)
    unidades = Column(Integer, nullable=False)   # número de unidades o parciales
    objetivo = Column(String, nullable=True)     # descripción breve
    idCarrera = Column(Integer, ForeignKey("carreras.idCarrera"))

    # Relación con Carrera
    carrera = relationship("Carrera", back_populates="materias")
    # Relación con GrupoMateria
    grupos = relationship("GrupoMateria", back_populates="materia")


class GrupoMateria(Base):
    __tablename__ = "grupo_materias"

    idGrupoMateria = Column(Integer, primary_key=True, index=True)
    idGrupo = Column(Integer, ForeignKey("grupos.idGrupo"))
    idMateria = Column(Integer, ForeignKey("materias.idMateria"))

    # Relación con Grupo
    grupo = relationship("Grupo", back_populates="materias")
    # Relación con Materia
    materia = relationship("Materia", back_populates="grupos")



class Calificacion(Base):
    __tablename__ = "calificaciones"

    idCalificacion = Column(Integer, primary_key=True, index=True)
    idAlumno = Column(Integer, ForeignKey("alumnos.idAlumno"))
    idMateria = Column(Integer, ForeignKey("materias.idMateria"))
    idDocente = Column(Integer, ForeignKey("docentes.idDocente"))

    calUnidad1 = Column(Integer, nullable=True)
    calUnidad2 = Column(Integer, nullable=True)
    calUnidad3 = Column(Integer, nullable=True)

    # Relaciones
    alumno = relationship("Alumno", back_populates="calificaciones")
    materia = relationship("Materia")
    docente = relationship("Docente")


class Asistencia(Base):
    __tablename__ = "asistencias"

    idAsistencia = Column(Integer, primary_key=True, index=True)
    idAlumno = Column(Integer, ForeignKey("alumnos.idAlumno"))
    idMateria = Column(Integer, ForeignKey("materias.idMateria"))
    idDocente = Column(Integer, ForeignKey("docentes.idDocente"))

    fecha = Column(Date, nullable=False)
    asistencia = Column(Boolean, default=True)  # True = asistió, False = falta

    # Relaciones
    alumno = relationship("Alumno", back_populates="asistencias")
    materia = relationship("Materia")
    docente = relationship("Docente")





class Token(Base):
    __tablename__ = "tokens"

    idToken = Column(Integer, primary_key=True, index=True)
    idUsuario = Column(Integer, ForeignKey("usuarios.idUsuario"))
    token = Column(String, unique=True, nullable=False)
    fechaGeneracion = Column(DateTime, default=datetime.datetime.utcnow)
    fechaExpiracion = Column(DateTime, nullable=False)
    utilizado = Column(Boolean, default=False)

    # Relación con Usuario
    usuario = relationship("Usuario")

