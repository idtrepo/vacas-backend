from decimal import Decimal
from datetime import date, time
from pydantic import BaseModel


class DataBase(BaseModel):
    ns:int
    fecha:date|None
    hora:time|None
    lat:str|None
    lon:str|None
    pasos:int
    tempA:Decimal
    tempO:Decimal
    rssi:int
    snr:int


class DataLeer(DataBase):
    id:int


class DataCrear(DataBase):
    pass


class DataEditar(BaseModel):
    ns:int|None = None
    fecha:date|None = None
    hora:time|None = None
    lat:str|None = None
    lon:str|None = None
    pasos:int|None = None
    tempA:Decimal|None = None
    tempO:Decimal|None = None
    rssi:int|None = None
    snr:int|None = None