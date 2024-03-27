from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, status
from config.settings import SECRET_KEY
from apps.auth.helpers.constantes import ALGORITMO


def crear_token(data:dict, expiracion:timedelta) -> str:
    datos = data.copy()

    tiempo_expiracion = datetime.now(timezone.utc) + expiracion

    datos.update({'exp': tiempo_expiracion})

    return jwt.encode(datos, SECRET_KEY, ALGORITMO)


def decodificar_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])

        return payload
    except JWTError:
        print('HUBO PEDo en decodificar token')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales invalidas'
        )