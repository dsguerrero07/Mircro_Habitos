from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app import models
from app.routers import usuarios, microrretos, progreso, gamificacion, comunidad, reportes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plataforma Digital de Micro Hábitos de Conocimiento",
    version="1.0.0",
    description="API educativa desarrollada por Duván Guerrero"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(usuarios.router)
app.include_router(microrretos.router)
app.include_router(progreso.router)
app.include_router(gamificacion.router)
app.include_router(comunidad.router)
app.include_router(reportes.router)
