"""
Archivo: main.py
Descripción: Inicia la aplicación FastAPI, conecta routers, templates y base de datos
"""

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app import models

from app.routers import usuarios, microrretos, progreso, gamificacion, comunidad, reportes

# ✅ ESTA LÍNEA ES LA CLAVE (CREA LAS TABLAS AUTOMÁTICAMENTE)
Base.metadata.create_all(bind=engine)

# ✅ Crear UNA sola instancia de FastAPI
app = FastAPI(
    title="Plataforma Digital de Micro Hábitos de Conocimiento",
    version="1.0.0",
    description="API educativa desarrollada por Duván Guerrero"
)

# ✅ Static files (CSS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ✅ Templates HTML
templates = Jinja2Templates(directory="app/templates")

# ✅ Ruta principal HTML
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Conectar routers
app.include_router(usuarios.router)
app.include_router(microrretos.router)
app.include_router(progreso.router)
app.include_router(gamificacion.router)
app.include_router(comunidad.router)
app.include_router(reportes.router)
