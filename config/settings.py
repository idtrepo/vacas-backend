from dotenv import load_dotenv, dotenv_values
import os


load_dotenv()
env_dir = dotenv_values('.env')

print('VARIABLES DE ENTORNO')
print(env_dir)

DB_USER = env_dir.get('DB_USER')
DB_PASS = env_dir.get('DB_PASS')
DB_HOST = env_dir.get('DB_HOST')
DB_PORT = env_dir.get('DB_PORT')
DB_NAME = env_dir.get('DB_NAME')
DB_DRIVER = env_dir.get('DB_DRIVER')
SECRET_KEY = env_dir.get('SECRET_KEY')


def obtener_db_conexion():
    return f'{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'