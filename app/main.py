"""
Archivo: main.py
Descripción: Inicia la aplicación FastAPI y conecta los routers

"""

from fastapi import FastAPI
from app import models, database
from app.routers import usuario
from app.routers import microrreto
from app.routers import progreso
from app.routers import gamificacion
from app.routers import comunidad

# Crea las tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

# Crea la aplicación principal
app = FastAPI(
    title="Plataforma Digital de Micro Hábitos de Conocimiento",
    version="1.0.0",
    description="API educativa desarrollada por Duván Guerrero"
)

# Conecta las rutas (routers)
app.include_router(usuario.router)
app.include_router(microrreto.router)
app.include_router(progreso.router)
app.include_router(gamificacion.router)
app.include_router(comunidad.router)
