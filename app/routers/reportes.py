from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

templates = Jinja2Templates(directory="app/templates")

# ==========================================================
#  DASHBOARD PRINCIPAL
# ==========================================================
@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):

    total_usuarios = db.query(func.count(models.Usuario.id)).scalar()
    total_progresos = db.query(func.count(models.Progreso.id)).scalar()
    total_retos = db.query(func.count(models.MicroReto.id)).scalar()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuarios": total_usuarios,
            "progresos": total_progresos,
            "retos": total_retos
        }
    )

# ==========================================================
#  GENERAR Y DESCARGAR PDF DE RANKING (MULTIMEDIA ✅)
# ==========================================================
@router.get("/ranking", summary="Genera un PDF con el ranking de usuarios por puntos")
def generar_reporte_ranking(db: Session = Depends(get_db)):

    ranking = db.query(models.Gamificacion).order_by(
        models.Gamificacion.puntos.desc()
    ).all()

    if not ranking:
        raise HTTPException(status_code=404, detail="No hay datos para generar el ranking")

    carpeta = "app/static/reportes"
    os.makedirs(carpeta, exist_ok=True)

    archivo = "ranking_usuarios.pdf"
    ruta = os.path.join(carpeta, archivo)

    pdf = canvas.Canvas(ruta, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(150, 750, "Ranking de Usuarios por Puntos")

    pdf.setFont("Helvetica", 12)
    y = 700

    pdf.drawString(50, y, "Puesto")
    pdf.drawString(120, y, "Usuario")
    pdf.drawString(300, y, "Puntos")
    pdf.drawString(400, y, "Badge")

    y -= 30
    puesto = 1

    for item in ranking:
        usuario = db.query(models.Usuario).filter(
            models.Usuario.id == item.usuario_id
        ).first()

        if not usuario:
            continue

        pdf.drawString(50, y, str(puesto))
        pdf.drawString(120, y, usuario.nombre)
        pdf.drawString(300, y, str(item.puntos))
        pdf.drawString(400, y, item.badge)

        puesto += 1
        y -= 25

        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()

    return FileResponse(
        path=ruta,
        filename="ranking_usuarios.pdf",
        media_type="application/pdf"
    )

# ==========================================================
#  VISTA HTML DE REPORTES
# ==========================================================
@router.get("/vista")
def vista_reportes(request: Request):
    return templates.TemplateResponse(
        "reportes.html",
        {"request": request}
    )
