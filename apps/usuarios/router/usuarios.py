from typing import Annotated
from fastapi import APIRouter, status, Depends, Path, Body, HTTPException
from sqlmodel import Session, select
from config.db import obtener_sesion
from apps.base.helpers.password import hashear_password
from apps.base.helpers.respuestas import generar_respuesta, generar_respuesta_error, Metodos
from ..schemas.usuarios import (UsuarioLeer, UsuarioCrear, UsuarioEditar)
from ..models.usuarios import Usuario


router = APIRouter(
    prefix='/usuarios',
    tags=['usuarios']
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[UsuarioLeer]
)
def obtener_usuarios(
    sesion:Annotated[Session, Depends(obtener_sesion)]
):
    query = select(Usuario)
    usuarios_db = sesion.exec(query).all()

    return usuarios_db


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=UsuarioLeer
)
def obtener_usuario(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)]
):
    usuario_db = sesion.get(Usuario, id)

    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario no encontrado')

    return usuario_db


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UsuarioLeer
)
def crear_usuario(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    usuario:Annotated[UsuarioCrear, Body()]
):
    try:
        nuevo_usuario = Usuario.model_validate(usuario)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Los datos del usuario son invalidos')

    nuevo_usuario.password = hashear_password(nuevo_usuario.password)
    
    sesion.add(nuevo_usuario)
    sesion.commit()
    sesion.refresh(nuevo_usuario)
    
    return nuevo_usuario


@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=UsuarioLeer
)
def editar_usuario(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)],
    data_usuario:Annotated[UsuarioEditar, Body()]
):
    usuario_db = sesion.get(Usuario, id)
    
    if usuario_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario no encontrado')

    usuario_db.nombre = data_usuario.nombre or usuario_db.nombre
    usuario_db.apellido = data_usuario.apellido or usuario_db.apellido
    usuario_db.correo = data_usuario.correo or usuario_db.correo

    if data_usuario.password is not None:
        usuario_db.password = hashear_password(data_usuario.password)

    sesion.add(usuario_db)
    sesion.commit()
    sesion.refresh(usuario_db)

    return usuario_db