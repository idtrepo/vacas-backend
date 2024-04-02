from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from apps.base.models.base import Base


if TYPE_CHECKING:
    from apps.data.models.data import Data
    from apps.vacas.models.vacas import Vaca



class Dispositivo(Base, table=True):
    id:int|None = Field(default=None, primary_key=True)
    ns:int

    datos:list['Data'] = Relationship(back_populates='dispositivo')
    vaca:Optional['Vaca'] = Relationship(back_populates='dispositivo')