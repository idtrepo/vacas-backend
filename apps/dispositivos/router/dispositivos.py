from typing import Annotated
from fastapi import APIRouter, status, Depends, Path, Query, Body, HTTPException
from sqlmodel import Session, select
from apps.dispositivos.schemas.dispositivos import DispositivoLeer, DispositivoCrear, DispositivoEditar
from config.db import obtener_sesion
from apps.dispositivos.models.dispositivos import Dispositivo
from apps.auth.dependencias.autenticacion import autenticar_usuario


router = APIRouter(
    prefix='/dispositivos',
    tags=['dispositivos'],
    # dependencies=[Depends(autenticar_usuario)]
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[DispositivoLeer]
)
def obtener_dispositivos(
    sesion:Annotated[Session, Depends(obtener_sesion)]
):
    dispositivos_db = sesion.exec(select(Dispositivo)).all()

    return dispositivos_db


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=DispositivoLeer
)
def obtener_dispositivo(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)]
):
    dispositivo_db = sesion.get(Dispositivo, id)

    if dispositivo_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dispositivo no encontrado'
        )
    
    return dispositivo_db


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=DispositivoLeer
)
def crear_dispositivo(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    dispositivo:Annotated[DispositivoCrear, Body()]
):
    nuevo_dispositivo = Dispositivo.model_validate(dispositivo)

    sesion.add(nuevo_dispositivo)
    sesion.commit()
    sesion.refresh(nuevo_dispositivo)

    return nuevo_dispositivo


@router.patch(
    '/{id}',
    response_model=DispositivoLeer,
    status_code=status.HTTP_200_OK
)
def editar_dispositivo(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    id:Annotated[int, Path(gt=0)],
    dispositivo:Annotated[DispositivoEditar, Body()]
):
    dispositivo_db = sesion.get(Dispositivo, id)

    if dispositivo_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dispositivo no encontrado'
        )
    
    dispositivo_db.ns = dispositivo.ns or dispositivo_db.ns

    sesion.add(dispositivo_db)
    sesion.commit()
    sesion.refresh(dispositivo_db)

    return dispositivo_db