from typing import Annotated, Any
from fastapi import APIRouter, status, Depends, Path, Body, Query, HTTPException
from sqlmodel import Session, select
from apps.dispositivos.models.dispositivos import Dispositivo
from apps.data.models.data import Data
from apps.data.schemas.data import DataCrear, DataEditar, DataLeer
from config.db import obtener_sesion
from apps.auth.dependencias.autenticacion import autenticar_usuario


router = APIRouter(
    prefix='/data',
    tags=['data'],
    dependencies=[Depends(autenticar_usuario)]
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[DataLeer]
)
def obtener_datos(
    sesion:Annotated[Session, Depends(obtener_sesion)]
):
    data_db = sesion.exec(
        select(Data)
    )
    return data_db



@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=dict
)
def crear_data(
    sesion:Annotated[Session, Depends(obtener_sesion)],
    data:Annotated[list[DataCrear], Body()]
):
    for dataVaca in data:
        dispositivo_db = sesion.exec(
            select(Dispositivo).where(Dispositivo.ns == dataVaca.ns)
        ).first()

        if dispositivo_db is None:
            continue

        try:
            nueva_data = Data.model_validate(dataVaca)
            nueva_data.dispositivo = dispositivo_db
            sesion.add(nueva_data)
        except Exception as e:
            print('Error en el formato')
            continue

    sesion.commit()

    return {
        'mensaje': 'Datos guardados con exito'
    }