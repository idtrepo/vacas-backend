from dotenv import load_dotenv, dotenv_values


load_dotenv()
env_data = {**dotenv_values('.env')}


DB_USER = env_data.get('DB_USER')
DB_PASS = env_data.get('DB_PASS')
DB_HOST = env_data.get('DB_HOST')
DB_PORT = env_data.get('DB_PORT')
DB_NAME = env_data.get('DB_NAME')
DB_DRIVER = env_data.get('DB_DRIVER')

SECRET_KEY = env_data.get('SECRET_KEY')


def obtener_db_conexion():
    return f'{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'