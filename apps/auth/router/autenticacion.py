from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, status, Body, Depends, HTTPException
from sqlmodel import Session
from config.db import obtener_sesion
from apps.usuarios.schemas.usuarios import UsuarioLeer
from apps.auth.schemas.autenticacion import UsuarioLogin, Token, TokenAccess, TokenActualizar
from apps.auth.helpers.autenticar import autenticar_usuario, obtener_usuario
from apps.auth.helpers.token import crear_token, decodificar_token
from apps.auth.helpers.constantes import EXPIRACION_TOKEN_ACCESS, EXPIRACION_TOKEN_REFRESH


router = APIRouter(
    prefix='/autenticacion',
    tags=['autenticacion']
)


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=Token
)
def iniciar_sesion(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    usuario:Annotated[UsuarioLogin, Body()]
):
    usuario_db = autenticar_usuario(
        sesion,
        usuario.correo,
        usuario.password
    )

    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Las credenciales proveidas no son correctas'
        )

    usuario = UsuarioLeer(**usuario_db.model_dump())
    data_usuario = {'usuario': usuario.model_dump()}
    token_access = crear_token(data_usuario, timedelta(minutes=EXPIRACION_TOKEN_ACCESS))
    token_refresh = crear_token(data_usuario, timedelta(hours=EXPIRACION_TOKEN_REFRESH))

    return Token(
        access=token_access,
        refresh=token_refresh
    )


@router.post(
    '/actualizar',
    status_code=status.HTTP_200_OK, 
    response_model=TokenAccess
)
def actualizar_sesion(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    token:Annotated[TokenActualizar, Body()]
):
    payload = decodificar_token(token.refresh)
    correo = payload.get('usuario').get('correo')

    usuario_db = obtener_usuario(sesion, correo)

    if not usuario_db:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    usuario = UsuarioLeer(**usuario_db.model_dump())
    data_usuario = {'usuario': usuario.model_dump()}
    token_access = crear_token(data_usuario, timedelta(minutes=EXPIRACION_TOKEN_ACCESS))

    return TokenAccess(access=token_access)