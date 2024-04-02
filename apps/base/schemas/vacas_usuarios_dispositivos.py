from pydantic import BaseModel, Field
from apps.base.schemas.base import SchemaBase
from apps.data.schemas.data import DataUbicacion


# Vacas
class VacaLeer(SchemaBase):
    id:int
    nombre:str
    peso:float
    anios:int
    meses:int


class VacaCrear(BaseModel):
    nombre:str
    peso:float
    anios:int
    meses:int
    usuario:int = Field(gt=0)
    dispositivo:int = Field(gt=0)


class VacaEditar(BaseModel):
    nombre:str|None = None
    peso:float|None = None
    anios:int|None = None
    meses:int|None = None


class VacaDispositivoLeer(BaseModel):
    id:int
    nombre:str


# Usuarios
class UsuarioLeer(SchemaBase):
    id:int
    nombre:str
    apellido:str
    correo:str
    vacas:list[VacaLeer] = []


class UsuarioVacaLeer(BaseModel):
    id:int
    nombre:str
    apellido:str
    correo:str


class UsuarioCrear(BaseModel):
    nombre:str
    apellido:str
    correo:str
    password:str


class UsuarioEditar(BaseModel):
    nombre:str|None = None
    apellido:str|None = None
    correo:str|None = None
    password:str|None = None


# Dispositivos
class DispositivoLeer(SchemaBase):
    id:int
    ns:int
    vaca:VacaDispositivoLeer|None = None


class DispositivoData(BaseModel):
    id:int
    ns:int
    datos:list[DataUbicacion] = []


class DispositivoCrear(BaseModel):
    ns:int


class DispositivoEditar(BaseModel):
    ns:int|None = None


class VacaDispositivoUbicacion(BaseModel):
    id:int
    nombre:str 
    dispositivo:DispositivoData|None = None