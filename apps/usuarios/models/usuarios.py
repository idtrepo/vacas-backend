from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from apps.base.models.base import Base
from apps.vacas.models.vacas import Vaca


class Usuario(Base, table=True):
    id:int|None = Field(default=None, primary_key=True)
    correo:str = Field(unique=True)
    nombre:str
    apellido:str
    password:str 

    vacas:list[Vaca] = Relationship(back_populates='usuario')