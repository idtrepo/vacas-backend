from typing import Annotated
from fastapi import APIRouter, status, Depends, Path, Body
from sqlmodel import Session, select
from config.db import obtener_sesion
from apps.base.helpers.password import hashear_password
from apps.base.helpers.respuestas import generar_respuesta, generar_respuesta_error, Metodos
from ..schemas.usuarios import (UsuarioLeer, UsuarioCrear, UsuarioEditar, RespuestaLeer, RespuestaListado)
from ..models.usuarios import Usuario


router = APIRouter(
    prefix='/usuarios',
    tags=['usuarios']
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=RespuestaListado
)
def obtener_usuarios(
    sesion:Annotated[Session, Depends(obtener_sesion)]
):
    query = select(Usuario)
    usuarios_db = sesion.exec(query).all()
    instancia = usuarios_db[0] if len(usuarios_db) > 0 else Usuario()

    return generar_respuesta(
        instancia=instancia, 
        data=usuarios_db, 
        metodo=Metodos.LISTADO.value
    )


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=RespuestaLeer
)
def obtener_usuario(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)]
):
    usuario_db = sesion.get(Usuario, id)

    if usuario_db is None:
        raise generar_respuesta_error(
            instancia=Usuario(), 
            metodo=Metodos.UNICO.value
        )

    return generar_respuesta(
        instancia=usuario_db, 
        data=usuario_db, 
        metodo=Metodos.UNICO.value
    )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaLeer
)
def crear_usuario(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    data_usuario:Annotated[UsuarioCrear, Body()]
):
    try:
        nuevo_usuario = Usuario.model_validate(data_usuario)
    except Exception as e:
        raise generar_respuesta_error(
            instancia=Usuario(), 
            metodo=Metodos.VALIDACION.value
        )

    nuevo_usuario.password = hashear_password(nuevo_usuario.password)
    
    try:
        sesion.add(nuevo_usuario)
        sesion.commit()
        sesion.refresh(nuevo_usuario)

        return generar_respuesta(
            instancia=nuevo_usuario, 
            data=nuevo_usuario, 
            metodo=Metodos.CREAR.value
        )
    except Exception as e:
        print(e)
        raise generar_respuesta_error(
            instancia=Usuario(), 
            metodo=Metodos.CREAR.value
        )


@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=RespuestaLeer
)
def editar_usuario(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)],
    data_usuario:Annotated[UsuarioEditar, Body()]
):
    usuario_db = sesion.get(Usuario, id)
    
    if usuario_db is None:
        raise generar_respuesta_error(
            instancia=Usuario(),  
            metodo=Metodos.UNICO.value
        )

    usuario_db.nombre = data_usuario.nombre or usuario_db.nombre
    usuario_db.apellido = data_usuario.apellido or usuario_db.apellido
    usuario_db.correo = data_usuario.correo or usuario_db.correo

    if data_usuario.password is not None:
        usuario_db.password = hashear_password(data_usuario.password)

    try:
        sesion.add(usuario_db)
        sesion.commit()
        sesion.refresh(usuario_db)

        return generar_respuesta(
            instancia=usuario_db, 
            data=usuario_db, 
            metodo=Metodos.EDITAR.value
        )
    except Exception as e:
        print(e)
        raise generar_respuesta_error(
            instancia=Usuario(), 
            metodo=Metodos.EDITAR.value
        )