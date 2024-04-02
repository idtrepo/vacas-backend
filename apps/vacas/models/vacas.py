from typing import TYPE_CHECKING, Optional
from decimal import Decimal
from sqlmodel import Field, Relationship
from apps.base.models.base import Base


if TYPE_CHECKING:
    from apps.usuarios.models.usuarios import Usuario 
    from apps.dispositivos.models.dispositivos import Dispositivo


class Vaca(Base, table=True):
    id:int|None = Field(default=None, primary_key=True)
    nombre:str 
    peso:Decimal = Field(default=0, max_digits=6, decimal_places=2)
    anios:int
    meses:int

    usuario_id:int|None = Field(default=None, foreign_key='usuario.id')
    usuario:Optional['Usuario'] = Relationship(back_populates='vacas')
    dispositivo_id:int|None = Field(default=None, foreign_key='dispositivo.id')
    dispositivo:Optional['Dispositivo'] = Relationship(back_populates='vaca')