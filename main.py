from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from config.db import crear_db
from apps.usuarios.router import usuarios
from apps.vacas.router import vacas
from apps.dispositivos.router import dispositivos
from apps.data.router import data
from apps.auth.router import autenticacion


origins = [
    '*',
    # 'http://localhost',
    # 'http://127.0.0.0',
    # 'http://localhost:5173',
]

@asynccontextmanager
async def lifespan(app:FastAPI):
    crear_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.middleware('http')
async def verificar_request(request:Request, call_next):
    print('hola desde el middleware')
    print(request.headers)
    print(request.method)
    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(data.router, prefix='/api')
app.include_router(vacas.router, prefix='/api')
app.include_router(usuarios.router, prefix='/api')
app.include_router(dispositivos.router, prefix='/api')
app.include_router(autenticacion.router, prefix='/api')


@app.get('/')
def index():
    return {'mensaje': 'hola mundo'}