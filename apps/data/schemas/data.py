from decimal import Decimal
from datetime import date, time, datetime
from pydantic import BaseModel


class DataLeer(BaseModel):
    id:int
    ns:int
    fecha:date
    hora:time
    lat:Decimal
    lon:Decimal
    pasos:int
    tempA:Decimal
    tempO:Decimal
    bat:Decimal
    rssi:int
    snr:int
    estatus:bool
    creado:datetime
    editado:datetime


class DataUbicacion(BaseModel):
    id:int
    fecha:date
    hora:time
    lat:Decimal
    lon:Decimal
    pasos:int
    tempA:Decimal
    tempO:Decimal
    creado:datetime


class DataCrear(BaseModel):
    ns:int
    fecha:date|None = None
    hora:time|None = None
    lat:Decimal
    lon:Decimal
    pasos:int
    tempA:Decimal
    tempO:Decimal
    bat:Decimal
    rssi:int
    snr:int


class DataEditar(BaseModel):
    ns:int|None = None
    fecha:date|None = None
    hora:time|None = None
    lat:Decimal|None = None
    lon:Decimal|None = None
    pasos:int|None = None
    tempA:Decimal|None = None
    tempO:Decimal|None = None
    bat:Decimal|None = None
    rssi:int|None = None
    snr:int|None = None