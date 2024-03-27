from typing import TYPE_CHECKING, Optional
from decimal import Decimal
from datetime import datetime, date, time
from sqlmodel import SQLModel, Field, Relationship


class Perfil(SQLModel, table=True):
    id:int|None = Field(default=None, primary_key=True)