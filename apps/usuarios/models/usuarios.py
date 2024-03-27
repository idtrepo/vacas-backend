from sqlmodel import SQLModel, Field, Relationship
from apps.vacas.models.vacas import Vaca


class Usuario(SQLModel, table=True):
    id:int|None = Field(default=None, primary_key=True)
    correo:str = Field(unique=True)
    nombre:str
    apellido:str
    password:str 

    vacas:list[Vaca] = Relationship(back_populates='usuario')