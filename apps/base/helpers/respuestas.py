from enum import Enum
from fastapi import status, HTTPException


class Metodos(Enum):
    UNICO = 'unico'
    LISTADO = 'listado'
    CREAR = 'crear'
    EDITAR = 'editar'
    ELIMINAR = 'eliminar',
    VALIDACION = 'validacion'


MENSAJES = {
    'unico': lambda nombre:f'Registro de {nombre} obtenido',
    'listado': lambda nombre:f'Listado de {nombre}s obtenido',
    'crear': lambda nombre:f'Registro de {nombre} creado',
    'editar': lambda nombre:f'Registro de {nombre} editado',
    'eliminar': lambda nombre:f'Registro de {nombre} eliminado'
}


def generar_respuesta(instancia, data, metodo):
    nombre_instancia = instancia.__class__.__name__
    mensaje = MENSAJES[metodo](nombre_instancia)

    return {
        'mensaje': mensaje,
        'data': data
    }


MENSAJES_ERROR = {
    'unico': lambda nombre:f'Registro de {nombre} no encontrado',
    'listado': lambda nombre:f'Listado de {nombre}s no encontrados',
    'crear': lambda nombre:f'Registro de {nombre} sin crear',
    'editar': lambda nombre:f'Registro de {nombre} sin editar',
    'eliminar': lambda nombre:f'Registro de {nombre} sin eliminar',
    'validacion': lambda nombre:f'Registro de {nombre} no tiene los datos correctos',
}

ESTATUS_ERROR = {
    'unico': status.HTTP_404_NOT_FOUND,
}


def generar_respuesta_error(instancia, metodo):
    nombre_instancia = instancia.__class__.__name__
    mensaje = MENSAJES_ERROR[metodo](nombre_instancia)

    return HTTPException(
        status_code=ESTATUS_ERROR.get(metodo, status.HTTP_400_BAD_REQUEST),
        detail=mensaje
    )