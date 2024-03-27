from pydantic import BaseModel


class UsuarioLogin(BaseModel):
    correo:str
    password:str


class Token(BaseModel):
    access:str
    refresh:str


class TokenActualizar(BaseModel):
    refresh:str


class TokenAccess(BaseModel):
    access:str