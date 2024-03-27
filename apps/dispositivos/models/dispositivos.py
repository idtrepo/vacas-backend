from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from apps.data.models.data import Data
    from apps.vacas.models.vacas import Vaca



class Dispositivo(SQLModel, table=True):
    id:int|None = Field(default=None, primary_key=True)
    ns:int

    datos:list['Data'] = Relationship(back_populates='dispositivo')
    vaca_id:int|None = Field(default=None, foreign_key='vaca.id')
    vaca:Optional['Vaca'] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates='dispositivo'
    )