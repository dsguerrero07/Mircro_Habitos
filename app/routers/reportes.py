from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

@router.get("/ranking", summary="Genera un PDF con el ranking de usuarios por puntos")
def generar_reporte_ranking(db: Session = Depends(get_db)):

    # Obtener usuarios ordenados por puntos (descendente)
    ranking = db.query(models.Gamificacion).order_by(models.Gamificacion.puntos.desc()).all()

    # Crear archivo PDF
    archivo = "ranking_usuarios.pdf"
    pdf = canvas.Canvas(archivo, pagesize=letter)

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
        usuario = db.query(models.Usuario).filter(models.Usuario.id == item.usuario_id).first()

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

    return {"mensaje": "Reporte generado exitosamente", "archivo": archivo}
