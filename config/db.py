from sqlmodel import SQLModel, Session, create_engine
from config.settings import obtener_db_conexion
from apps.usuarios.models import usuarios
from apps.vacas.models import vacas
from apps.dispositivos.models import dispositivos
from apps.data.models import data


db_conexion = obtener_db_conexion()
engine = create_engine(db_conexion)


def crear_db():
    SQLModel.metadata.create_all(engine)


def obtener_sesion():
    with Session(engine) as sesion:
        yield sesion