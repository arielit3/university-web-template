from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
import random
from schemas import (
    CarreraCreate, UsuarioCreate, AlumnoCreate, DocenteCreate,
    DirectorCreate, MateriaCreate, GrupoCreate, GrupoMateriaCreate,
    CalificacionCreate
)

router = APIRouter(
    prefix="/seed",
    tags=["seed"]
)

@router.post("/")
def generar_seed(db: Session = Depends(get_db)):
    # --- Crear carreras ---
    carrera1 = crud.crear_carrera(db, CarreraCreate(nombreCarrera="Ingenieria en Sistemas", planEstudios=2022))
    carrera2 = crud.crear_carrera(db, CarreraCreate(nombreCarrera="Administracion de Empresas", planEstudios=2021))
    carrera3 = crud.crear_carrera(db, CarreraCreate(nombreCarrera="Arquitectura", planEstudios=2023))

    # --- Crear directores ---
    director1_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Mario", apellido="Lopez",
        correo=f"Nort_{random.randint(100,999)}te@USN.com",
        contraseña="lopez123", tipo="director"
    ))
    director1 = crud.crear_director(db, DirectorCreate(idUsuario=director1_user.idUsuario, idCarrera=carrera1.idCarrera))

    director2_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Jose", apellido="Martinez",
        correo=f"Nort_{random.randint(100,999)}te@USN.com",
        contraseña="martinez123", tipo="director"
    ))
    director2 = crud.crear_director(db, DirectorCreate(idUsuario=director2_user.idUsuario, idCarrera=carrera2.idCarrera))

    director3_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Luis", apellido="Garcia",
        correo=f"Nort_{random.randint(100,999)}te@USN.com",
        contraseña="garcia123", tipo="director"
    ))
    director3 = crud.crear_director(db, DirectorCreate(idUsuario=director3_user.idUsuario, idCarrera=carrera3.idCarrera))

    # --- Crear docentes ---
    docente1_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Carlos", apellido="Ramirez",
        correo=f"Nort_{random.randint(100,999)}te@USN.com",
        contraseña="ramirez123", tipo="docente"
    ))
    docente1 = crud.crear_docente(db, DocenteCreate(idUsuario=docente1_user.idUsuario, idCarrera=carrera1.idCarrera, nivelEstudios="Maestria", turno="Matutino"))

    docente2_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Miguel", apellido="Torres",
        correo=f"Nort_{random.randint(100,999)}te@USN.com",
        contraseña="torres123", tipo="docente"
    ))
    docente2 = crud.crear_docente(db, DocenteCreate(idUsuario=docente2_user.idUsuario, idCarrera=carrera1.idCarrera, nivelEstudios="Doctorado", turno="Vespertino"))

    # --- Crear grupos para carrera1 ---
    grupo1 = crud.crear_grupo(db, GrupoCreate(idCarrera=carrera1.idCarrera, idDocente=docente1.idDocente, nombreGrupo="SIS-101", periodo="2026-A", numAlumnos=30))
    grupo2 = crud.crear_grupo(db, GrupoCreate(idCarrera=carrera1.idCarrera, idDocente=docente2.idDocente, nombreGrupo="SIS-102", periodo="2026-A", numAlumnos=30))

    # --- Crear alumnos para grupo1 ---
    apellidos = ["Lopez", "Martinez", "Hernandez", "Garcia", "Ramirez", "Torres", "Flores", "Gomez", "Diaz", "Castro"]
    nombres = ["Juan", "Pedro", "Luis", "Carlos", "Miguel", "Jose", "David", "Jorge", "Manuel", "Ricardo"]

    for i in range(1, 31):
        apellido = random.choice(apellidos)
        nombre = random.choice(nombres)
        correo = f"Nort_{random.randint(100,999)}te@USN.com"
        contrasena = f"{apellido.lower()}123"

        usuario = crud.crear_usuario(db, UsuarioCreate(
            nombre=nombre, apellido=apellido,
            correo=correo, contraseña=contrasena, tipo="alumno"
        ))

        crud.crear_alumno(db, AlumnoCreate(
            idUsuario=usuario.idUsuario,
            idGrupo=grupo1.idGrupo,
            promedioPrep=round(random.uniform(7.0, 9.5), 2)
        ))

    # --- Crear materias por carrera ---
    materias_sistemas = [
        MateriaCreate(nombreMateria="Programacion I", unidades=3, objetivo="Fundamentos de programacion", idCarrera=carrera1.idCarrera),
        MateriaCreate(nombreMateria="Bases de Datos", unidades=3, objetivo="Diseno y administracion de BD", idCarrera=carrera1.idCarrera),
        MateriaCreate(nombreMateria="Redes", unidades=3, objetivo="Conceptos basicos de redes", idCarrera=carrera1.idCarrera)
    ]
    materias_admin = [
        MateriaCreate(nombreMateria="Contabilidad", unidades=3, objetivo="Principios de contabilidad", idCarrera=carrera2.idCarrera),
        MateriaCreate(nombreMateria="Marketing", unidades=3, objetivo="Fundamentos de marketing", idCarrera=carrera2.idCarrera),
        MateriaCreate(nombreMateria="Finanzas", unidades=3, objetivo="Gestion financiera", idCarrera=carrera2.idCarrera)
    ]
    materias_arq = [
        MateriaCreate(nombreMateria="Diseno Arquitectonico", unidades=3, objetivo="Principios de diseno", idCarrera=carrera3.idCarrera),
        MateriaCreate(nombreMateria="Historia del Arte", unidades=3, objetivo="Historia y estilos", idCarrera=carrera3.idCarrera),
        MateriaCreate(nombreMateria="Construccion", unidades=3, objetivo="Tecnicas de construccion", idCarrera=carrera3.idCarrera)
    ]

    for m in materias_sistemas + materias_admin + materias_arq:
        materia = crud.crear_materia(db, m)
        if m.idCarrera == carrera1.idCarrera:
            crud.crear_grupo_materia(db, GrupoMateriaCreate(idGrupo=grupo1.idGrupo, idMateria=materia.idMateria))

    # --- Crear calificaciones de prueba ---
    alumnos = crud.listar_alumnos(db)
    materias = crud.listar_materias(db)
    for alumno in alumnos[:5]:
        for materia in materias[:2]:
            crud.crear_calificacion(db, CalificacionCreate(
                idAlumno=alumno.idAlumno,
                idMateria=materia.idMateria,
                idDocente=docente1.idDocente,
                calUnidad1=round(random.uniform(7.0, 10.0), 2),
                calUnidad2=round(random.uniform(7.0, 10.0), 2),
                calUnidad3=round(random.uniform(7.0, 10.0), 2)
            ))

    return {"msg": "Seed generado con exito"}
