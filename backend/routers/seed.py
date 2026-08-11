from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
import random
from datetime import date
from schemas import (
    CarreraCreate, UsuarioCreate, AspiranteCreate, AlumnoCreate,
    DocenteCreate, MateriaCreate, GrupoCreate, GrupoMateriaCreate,
    CalificacionCreate, AsistenciaCreate
)
from auth import hash_password  # Importamos la función para encriptar contraseñas

router = APIRouter(
    prefix="/seed",
    tags=["seed"]
)

@router.post("/")
def generar_seed(db: Session = Depends(get_db)):
    # --- Crear directores ---
    director1 = crud.crear_usuario(db, UsuarioCreate(
        nombre="Mario", apellido="Lopez",
        correo="Nort_director1@USN.com", contraseña=hash_password("lopez123"), tipo="director"
    ))
    director2 = crud.crear_usuario(db, UsuarioCreate(
        nombre="Jose", apellido="Martinez",
        correo="Nort_director2@USN.com", contraseña=hash_password("martinez123"), tipo="director"
    ))
    director3 = crud.crear_usuario(db, UsuarioCreate(
        nombre="Luis", apellido="Garcia",
        correo="Nort_director3@USN.com", contraseña=hash_password("garcia123"), tipo="director"
    ))

    # --- Crear superadmin ---
    superadmin = crud.crear_usuario(db, UsuarioCreate(
        nombre="Super", apellido="Admin",
        correo="superadmin@USN.com", contraseña=hash_password("admin123"), tipo="admin"
    ))

    # --- Crear carreras con director asignado ---
    carrera1 = crud.crear_carrera(db, CarreraCreate(
        nombreCarrera="Ingenieria en Sistemas", planEstudios=2022, idDirector=director1.idUsuario
    ))
    carrera2 = crud.crear_carrera(db, CarreraCreate(
        nombreCarrera="Administracion de Empresas", planEstudios=2021, idDirector=director2.idUsuario
    ))
    carrera3 = crud.crear_carrera(db, CarreraCreate(
        nombreCarrera="Arquitectura", planEstudios=2023, idDirector=director3.idUsuario
    ))

    # --- Crear docentes ---
    docente1_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Carlos", apellido="Ramirez",
        correo="Nort_docente1@USN.com", contraseña=hash_password("ramirez123"), tipo="docente"
    ))
    docente1 = crud.crear_docente(db, DocenteCreate(
        idUsuario=docente1_user.idUsuario, idCarrera=carrera1.idCarrera,
        nivelEstudios="Maestria", turno="Matutino"
    ))

    docente2_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Miguel", apellido="Torres",
        correo="Nort_docente2@USN.com", contraseña=hash_password("torres123"), tipo="docente"
    ))
    docente2 = crud.crear_docente(db, DocenteCreate(
        idUsuario=docente2_user.idUsuario, idCarrera=carrera1.idCarrera,
        nivelEstudios="Doctorado", turno="Vespertino"
    ))

    # --- Crear grupos ---
    grupo1 = crud.crear_grupo(db, GrupoCreate(
        idCarrera=carrera1.idCarrera, idDocente=docente1.idDocente,
        nombreGrupo="SIS-101", periodo="2026-A", numAlumnos=30
    ))
    grupo2 = crud.crear_grupo(db, GrupoCreate(
        idCarrera=carrera1.idCarrera, idDocente=docente2.idDocente,
        nombreGrupo="SIS-102", periodo="2026-A", numAlumnos=30
    ))

    # --- Crear alumnos con correos únicos ---
    apellidos = ["Lopez", "Martinez", "Hernandez", "Garcia", "Ramirez", "Torres", "Flores", "Gomez", "Diaz", "Castro"]
    nombres = ["Juan", "Pedro", "Luis", "Carlos", "Miguel", "Jose", "David", "Jorge", "Manuel", "Ricardo"]

    for i in range(1, 31):
        apellido = random.choice(apellidos)
        nombre = random.choice(nombres)
        correo = f"Nort_alumno{i}@USN.com"  # único por índice
        contrasena = hash_password(f"{apellido.lower()}123")

        usuario = crud.crear_usuario(db, UsuarioCreate(
            nombre=nombre, apellido=apellido,
            correo=correo, contraseña=contrasena, tipo="alumno"
        ))

        crud.crear_alumno(db, AlumnoCreate(
            idUsuario=usuario.idUsuario,
            idGrupo=grupo1.idGrupo,
            promedioPrep=round(random.uniform(7.0, 9.5), 2)
        ))

    # --- Crear aspirantes de prueba ---
    aspirante1_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Ana", apellido="Sanchez",
        correo="Nort_aspirante1@USN.com", contraseña=hash_password("sanchez123"), tipo="aspirante"
    ))
    crud.crear_aspirante(db, AspiranteCreate(
        idUsuario=aspirante1_user.idUsuario,
        numFicha=1001,
        periodo="2026-A",
        carreraSolicita=carrera1.nombreCarrera,
        puntosExamen=88
    ))

    aspirante2_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Luis", apellido="Morales",
        correo="Nort_aspirante2@USN.com", contraseña=hash_password("morales123"), tipo="aspirante"
    ))
    crud.crear_aspirante(db, AspiranteCreate(
        idUsuario=aspirante2_user.idUsuario,
        numFicha=1002,
        periodo="2026-A",
        carreraSolicita=carrera2.nombreCarrera,
        puntosExamen=92
    ))

    aspirante3_user = crud.crear_usuario(db, UsuarioCreate(
        nombre="Mariana", apellido="Quintero",
        correo="Nort_aspirante3@USN.com", contraseña=hash_password("quintero123"), tipo="aspirante"
    ))
    crud.crear_aspirante(db, AspiranteCreate(
        idUsuario=aspirante3_user.idUsuario,
        numFicha=1003,
        periodo="2026-A",
        carreraSolicita=carrera3.nombreCarrera,
        puntosExamen=95
    ))

    # --- Crear materias ---
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

    # --- Crear asistencias de prueba ---
    for alumno in alumnos[:5]:
        crud.crear_asistencia(db, AsistenciaCreate(
            idAlumno=alumno.idAlumno,
            idMateria=materias[0].idMateria,
            idDocente=docente1.idDocente,
            fecha=date.today(),
            asistencia=True
        ))

    return {"msg": "Seed generado con exito"}
