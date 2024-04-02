from typing import TYPE_CHECKING, Optional
from decimal import Decimal
from datetime import datetime, date, time
from sqlmodel import Field, Relationship
from apps.base.models.base import Base


if TYPE_CHECKING:
    from apps.dispositivos.models.dispositivos import Dispositivo



class Data(Base, table=True):
    id:int|None = Field(default=None, primary_key=True)
    ns:int
    fecha:date|None = None
    hora:time|None = None
    lat:Decimal = Field(default=0, max_digits=9, decimal_places=6)
    lon:Decimal = Field(default=0, max_digits=9, decimal_places=6)
    pasos:int
    tempA:Decimal = Field(default=0, max_digits=5, decimal_places=2)
    tempO:Decimal = Field(default=0, max_digits=5, decimal_places=2)
    bat:Decimal = Field(default=0, max_digits=5, decimal_places=2)
    rssi:int
    snr:int

    dispositivo_id:int|None = Field(default=None, foreign_key='dispositivo.id')
    dispositivo:Optional['Dispositivo'] = Relationship(back_populates='datos')