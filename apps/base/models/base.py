from datetime import datetime
from sqlmodel import SQLModel, Field


class Base(SQLModel):
    estatus:bool = True
    creado:datetime|None = Field(default_factory=datetime.now)
    editado:datetime|None = Field(
        default_factory=datetime.now,
        sa_column_kwargs={
            'onupdate': datetime.now
        }
    )