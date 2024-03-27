from typing import Annotated
from fastapi import APIRouter, status, Path, Body, Depends
from sqlmodel import SQLModel, Session, select
from config.db import obtener_sesion
from apps.base.helpers.respuestas import generar_respuesta, generar_respuesta_error, Metodos
from apps.auth.dependencias.autenticacion import autenticar_usuario
from ..models.vacas import Vaca
from ..schemas.vacas import (RespuestaLeer, RespuestaListado, VacaCrear, VacaEditar)


router = APIRouter(
    prefix='/vacas',
    tags=['vacas'],
    dependencies=[Depends(autenticar_usuario)]
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=RespuestaListado
)
def obtener_vacas(
    sesion:Annotated[Session, Depends(obtener_sesion)]
):
    query = select(Vaca)
    vacas_db = sesion.exec(query).all()
    instancia = vacas_db[0] if len(vacas_db) > 0 else Vaca()

    return generar_respuesta(
        data=vacas_db,
        instancia=instancia,
        metodo=Metodos.LISTADO.value
    )


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=RespuestaLeer
)
def obtener_vaca(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)]
):
    vaca_db = sesion.get(Vaca, id)

    if vaca_db is None:
        raise generar_respuesta_error(
            instancia=Vaca(),
            metodo=Metodos.UNICO.value
        )

    return generar_respuesta(
        data=vaca_db,
        instancia=vaca_db,
        metodo=Metodos.UNICO.value
    )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaLeer
)
def crear_vaca(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    data_usuario:Annotated[VacaCrear, Body()]
):
    try:
        nueva_vaca = Vaca.model_validate(data_usuario)
    except Exception as e:
        print(e)
        raise generar_respuesta_error(
            instancia=Vaca(), 
            metodo=Metodos.VALIDACION.value
        )
    
    try:
        sesion.add(nueva_vaca)
        sesion.commit()
        sesion.refresh(nueva_vaca)

        return generar_respuesta(
            instancia=nueva_vaca, 
            data=nueva_vaca, 
            metodo=Metodos.CREAR.value
        )
    except Exception as e:
        print(e)
        raise generar_respuesta_error(
            instancia=Vaca(), 
            metodo=Metodos.CREAR.value
        )
    

@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=RespuestaLeer
)
def editar_vaca(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)],
    data_usuario:Annotated[VacaEditar, Body()]
):
    vaca_db = sesion.get(Vaca, id)
    
    if vaca_db is None:
        raise generar_respuesta_error(
            instancia=Vaca(),  
            metodo=Metodos.UNICO.value
        )

    vaca_db.peso = data_usuario.peso or vaca_db.peso
    vaca_db.nombre = data_usuario.nombre or vaca_db.nombre
    vaca_db.anios = data_usuario.anios or vaca_db.anios
    vaca_db.meses = data_usuario.meses or vaca_db.meses


    try:
        sesion.add(vaca_db)
        sesion.commit()
        sesion.refresh(vaca_db)

        return generar_respuesta(
            instancia=vaca_db, 
            data=vaca_db, 
            metodo=Metodos.EDITAR.value
        )
    except Exception as e:
        print(e)
        raise generar_respuesta_error(
            instancia=Vaca(), 
            metodo=Metodos.EDITAR.value
        )