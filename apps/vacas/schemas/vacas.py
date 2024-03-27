from pydantic import BaseModel


class VacaBase(BaseModel):
    nombre:str
    peso:float
    anios:int
    meses:int


class VacaLeer(VacaBase):
    id:int


class VacaCrear(VacaBase):
    pass


class VacaEditar(VacaBase):
    nombre:str|None = None
    peso:float|None = None
    anios:int|None = None
    meses:int|None = None


class RespuestaBase(BaseModel):
    mensaje:str


class RespuestaLeer(RespuestaBase):
    data:VacaLeer


class RespuestaListado(RespuestaBase):
    data:list[VacaLeer]