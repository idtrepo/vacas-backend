from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from config.db import obtener_sesion
from apps.auth.helpers.autenticar import obtener_token, obtener_usuario
from apps.auth.helpers.token import decodificar_token


def obtener_token_depend(token:Annotated[str, Depends(obtener_token)]):
    data = decodificar_token(token)
    usuario = data.get('usuario')
    correo = usuario.get('correo')

    return correo


def autenticar_usuario(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    correo:Annotated[str, Depends(obtener_token_depend)]
):
    usuario_db = obtener_usuario(sesion, correo)
    
    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales invalidas'
        )

