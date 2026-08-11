from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    correo: str
    tipo: str

class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioLogin(BaseModel):
    correo: str
    contraseña: str
    class Config:
        from_attributes = True

class UsuarioOut(UsuarioBase):
    idUsuario: int
    class Config:
        from_attributes = True

class AspiranteCreate(BaseModel):
    idUsuario: int
    numFicha: str
    periodo: str
    carreraSolicita: str
    puntosExamen: int

class AspiranteOut(AspiranteCreate):
    idAspirante: int
    class Config:
        from_attributes = True



from pydantic import BaseModel

class AlumnoCreate(BaseModel):
    idUsuario: int
    idGrupo: int
    promedioPrep: float

class AlumnoOut(AlumnoCreate):
    idAlumno: int
    class Config:
        from_attributes = True
from pydantic import BaseModel

class DocenteCreate(BaseModel):
    idUsuario: int
    idCarrera: int
    nivelEstudios: str
    turno: str

class DocenteOut(DocenteCreate):
    idDocente: int
    class Config:
        from_attributes = True

from pydantic import BaseModel

class CarreraCreate(BaseModel):
    nombreCarrera: str
    planEstudios: int
    idDirector: int | None = None

class CarreraOut(CarreraCreate):
    idCarrera: int
    class Config:
        from_attributes = True

from pydantic import BaseModel

class GrupoCreate(BaseModel):
    idCarrera: int
    idDocente: int
    nombreGrupo: str
    periodo: str
    numAlumnos: int

class GrupoOut(GrupoCreate):
    idGrupo: int
    class Config:
        from_attributes = True
from pydantic import BaseModel

class MateriaCreate(BaseModel):
    nombreMateria: str
    unidades: int
    objetivo: str
    idCarrera: int

class MateriaOut(MateriaCreate):
    idMateria: int
    class Config:
        from_attributes = True


from pydantic import BaseModel

class GrupoMateriaCreate(BaseModel):
    idGrupo: int
    idMateria: int

class GrupoMateriaOut(GrupoMateriaCreate):
    idGrupoMateria: int
    class Config:
        from_attributes = True
from pydantic import BaseModel

class CalificacionCreate(BaseModel):
    idAlumno: int
    idMateria: int
    idDocente: int
    calUnidad1: float
    calUnidad2: float
    calUnidad3: float

class CalificacionOut(CalificacionCreate):
    idCalificacion: int
    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import date

class AsistenciaCreate(BaseModel):
    idAlumno: int
    idMateria: int
    idDocente: int
    fecha: date
    asistencia: bool

class AsistenciaOut(AsistenciaCreate):
    idAsistencia: int
    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import datetime

class TokenCreate(BaseModel):
    idUsuario: int
    token: str
    fechaExpiracion: datetime
    utilizado: bool

class TokenOut(TokenCreate):
    idToken: int
    fechaGeneracion: datetime
    class Config:
        from_attributes = True
from pydantic import BaseModel


