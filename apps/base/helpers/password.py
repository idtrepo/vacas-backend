from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hashear_password(password):
    return pwd_context.hash(password)


def verificar_password(password, password_hasheado):
    return pwd_context.verify(password, password_hasheado)