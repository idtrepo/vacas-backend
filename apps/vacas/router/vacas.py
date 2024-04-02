from typing import Annotated
from fastapi import APIRouter, status, Path, Body, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from config.db import obtener_sesion
from apps.base.helpers.respuestas import generar_respuesta, generar_respuesta_error, Metodos
from apps.auth.dependencias.autenticacion import autenticar_usuario
from ..models.vacas import Vaca
from ..schemas.vacas import VacaCrear, VacaEditar, VacaLeer, VacaDispositivoUbicacion
from apps.dispositivos.models.dispositivos import Dispositivo
from apps.data.models.data import Data
from apps.usuarios.models.usuarios import Usuario


router = APIRouter(
    prefix='/vacas',
    tags=['vacas'],
    # dependencies=[Depends(autenticar_usuario)]
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[VacaLeer]
)
def obtener_vacas(
    sesion:Annotated[Session, Depends(obtener_sesion)]
):
    query = select(Vaca)
    vacas_db = sesion.exec(query).all()

    return vacas_db


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=VacaLeer
)
def obtener_vaca(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)]
):
    vaca_db = sesion.get(Vaca, id)

    if vaca_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Perfil de vaca no encontrado')

    return vaca_db


@router.get(
    '/{id}/ubicacion',
    status_code=status.HTTP_200_OK,
    # response_model=VacaDispositivoUbicacion
)
def obtener_ubicacion_vaca(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)]
):
    vaca_db = sesion.get(Vaca, id)

    if vaca_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Perfil de vaca no encontrado')
    
    dispositivo_db = sesion.exec(
        select(Dispositivo).where(Dispositivo.id == vaca_db.dispositivo_id)
    ).first()

    if dispositivo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dispositivo no encontrado')
    

    data_db = sesion.exec(
        select(Data).where(Data.dispositivo_id == dispositivo_db.id)
    ).all()

    return data_db


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=VacaLeer
)
def crear_vaca(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    vaca:Annotated[VacaCrear, Body()]
):
    print('INFO DE LA VACA A CREAR')
    print(vaca.model_dump())
    print('*' * 50)
    usuario_db = sesion.get(Usuario, vaca.usuario)
    dispositivo_db = sesion.get(Dispositivo, vaca.dispositivo)
    nueva_vaca = Vaca(
        peso=vaca.peso,
        anios=vaca.anios,
        meses=vaca.meses,
        nombre=vaca.nombre,
    )
    print('ACA TDBN 1')
    nueva_vaca.usuario = usuario_db
    nueva_vaca.dispositivo = dispositivo_db

    sesion.add(nueva_vaca)
    sesion.commit()
    sesion.refresh(nueva_vaca)

    return nueva_vaca
    

@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=VacaLeer
)
def editar_vaca(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)],
    data_usuario:Annotated[VacaEditar, Body()]
):
    vaca_db = sesion.get(Vaca, id)
    
    if vaca_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Perfil de vaca no encontrado')

    vaca_db.peso = data_usuario.peso or vaca_db.peso
    vaca_db.nombre = data_usuario.nombre or vaca_db.nombre
    vaca_db.anios = data_usuario.anios or vaca_db.anios
    vaca_db.meses = data_usuario.meses or vaca_db.meses

    sesion.add(vaca_db)
    sesion.commit()
    sesion.refresh(vaca_db)

    return VacaLeer