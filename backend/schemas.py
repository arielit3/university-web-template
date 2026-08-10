from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    correo: str
    tipo: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioOut(UsuarioBase):
    idUsuario: int
    class Config:
        orm_mode = True

class AspiranteCreate(BaseModel):
    idUsuario: int
    numFicha: str
    periodo: str
    carreraSolicita: str
    puntosExamen: int

class AspiranteOut(AspiranteCreate):
    idAspirante: int
    class Config:
        orm_mode = True



from pydantic import BaseModel

class AlumnoCreate(BaseModel):
    idUsuario: int
    idGrupo: int
    promedioPrep: float

class AlumnoOut(AlumnoCreate):
    idAlumno: int
    class Config:
        orm_mode = True
from pydantic import BaseModel

class DocenteCreate(BaseModel):
    idUsuario: int
    idCarrera: int
    nivelEstudios: str
    turno: str

class DocenteOut(DocenteCreate):
    idDocente: int
    class Config:
        orm_mode = True

from pydantic import BaseModel

class CarreraCreate(BaseModel):
    nombreCarrera: str
    planEstudios: int

class CarreraOut(CarreraCreate):
    idCarrera: int
    class Config:
        orm_mode = True

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
        orm_mode = True
from pydantic import BaseModel

class MateriaCreate(BaseModel):
    nombreMateria: str
    unidades: int
    objetivo: str
    idCarrera: int

class MateriaOut(MateriaCreate):
    idMateria: int
    class Config:
        orm_mode = True


from pydantic import BaseModel

class GrupoMateriaCreate(BaseModel):
    idGrupo: int
    idMateria: int

class GrupoMateriaOut(GrupoMateriaCreate):
    idGrupoMateria: int
    class Config:
        orm_mode = True
