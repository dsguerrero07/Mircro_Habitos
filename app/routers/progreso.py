from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/progreso", tags=["Progreso"])
templates = Jinja2Templates(directory="app/templates")

# ==========================================================
# ✅ Vista HTML del progreso
# ==========================================================
@router.get("/vista")
def ver_progreso(request: Request, db: Session = Depends(get_db)):
    datos = db.query(models.Progreso).all()
    return templates.TemplateResponse(
        "progreso.html",
        {"request": request, "progresos": datos}
    )

# ==========================================================
# ✅ Formulario HTML
# ==========================================================
@router.get("/nuevo")
def nuevo_progreso(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    retos = db.query(models.MicroReto).all()

    return templates.TemplateResponse(
        "crear_progreso.html",
        {
            "request": request,
            "usuarios": usuarios,
            "retos": retos
        }
    )

# ==========================================================
# ✅ Guardar progreso desde HTML
# ==========================================================
@router.post("/crear-html")
def crear_progreso_html(
    usuario_id: int = Form(...),
    reto_id: int = Form(...),
    completado: bool = Form(False),
    db: Session = Depends(get_db)
):
    nuevo = models.Progreso(
        usuario_id=usuario_id,
        reto_id=reto_id,
        completado=completado,
        fecha=datetime.utcnow()
    )

    db.add(nuevo)
    db.commit()

    return {"mensaje": "Progreso registrado correctamente"}
