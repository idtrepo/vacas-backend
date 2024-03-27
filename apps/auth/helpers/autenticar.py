from typing import Annotated
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from apps.base.helpers.password import verificar_password
from apps.usuarios.models.usuarios import Usuario
from apps.usuarios.schemas.usuarios import UsuarioLeer


# Obtenemos el token de los headers de la request
def obtener_token(authorization:Annotated[str|None, Header()] = None):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No cuentas con los permisos para ingresar'
        )

    _, token = authorization.split()

    return token


def obtener_usuario(sesion:Session, correo:str):
    usuario_db = sesion.exec(
        select(Usuario).where(Usuario.correo == correo)
    ).first()

    return usuario_db


def autenticar_usuario(sesion:Session, correo:str, password:str):
    usuario_db = obtener_usuario(sesion, correo)

    if not usuario_db:
        return False
    
    if not verificar_password(password, usuario_db.password):
        return False
    
    return usuario_db