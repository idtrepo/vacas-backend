from pydantic import BaseModel


class UsuarioBase(BaseModel):
    nombre:str
    apellido:str
    correo:str


class UsuarioCrear(UsuarioBase):
    password:str


class UsuarioLeer(UsuarioBase):
    id:int


class UsuarioEditar(BaseModel):
    nombre:str|None = None
    apellido:str|None = None
    correo:str|None = None
    password:str|None = None


class RespuestaBase(BaseModel):
    mensaje:str


class RespuestaLeer(RespuestaBase):
    data:UsuarioLeer


class RespuestaListado(RespuestaBase):
    data:list[UsuarioLeer]