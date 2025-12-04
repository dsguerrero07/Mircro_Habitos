from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
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
#  DASHBOARD HTML
# ==========================================================
@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    total_usuarios = db.query(models.Usuario).count()
    total_progresos = db.query(models.Progreso).count()
    total_retos = db.query(models.MicroReto).count()

    data = {
        "usuarios": total_usuarios,
        "progresos": total_progresos,
        "retos": total_retos
    }

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "data": data}
    )

# ==========================================================
#  GENERAR Y DESCARGAR PDF DE RANKING
# ==========================================================
@router.get("/ranking", summary="Genera un PDF con el ranking de usuarios por puntos")
def generar_reporte_ranking(db: Session = Depends(get_db)):

    ranking = db.query(models.Gamificacion).order_by(
        models.Gamificacion.puntos.desc()
    ).all()

    archivo = "ranking_usuarios.pdf"
    ruta = os.path.join(archivo)

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

@router.get("/vista")
def vista_reportes(request: Request):
    return templates.TemplateResponse(
        "reportes.html",
        {"request": request}
    )
