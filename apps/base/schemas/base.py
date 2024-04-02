from datetime import datetime
from pydantic import BaseModel


class SchemaBase(BaseModel):
    estatus:bool
    creado:datetime
    editado:datetime