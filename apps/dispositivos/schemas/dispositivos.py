from pydantic import BaseModel


class DispositivoBase(BaseModel):
    ns:int


class DispositivoLeer(DispositivoBase):
    id:int


class DispositivoCrear(DispositivoBase):
    pass


class DispositivoEditar(DispositivoBase):
    ns:int|None = None