from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/progreso",
    tags=["Progreso"]
)

# --------------------------------------------------------------
# Registrar avance (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Progreso, status_code=status.HTTP_201_CREATED)
def registrar_progreso(progreso: schemas.ProgresoCreate, db: Session = Depends(get_db)):
    """
    Registra el progreso de un usuario sobre un Microrreto.
    """

    # Validar existencia de usuario
    usuario = db.query(models.Usuario).filter(models.Usuario.id == progreso.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar existencia de reto
    reto = db.query(models.MicroReto).filter(models.MicroReto.id == progreso.reto_id).first()
    if not reto:
        raise HTTPException(status_code=404, detail="MicroReto no encontrado")

    nuevo_progreso = models.Progreso(
        usuario_id=progreso.usuario_id,
        reto_id=progreso.reto_id,
        completado=progreso.completado,
        fecha=progreso.fecha
    )

    db.add(nuevo_progreso)
    db.commit()
    db.refresh(nuevo_progreso)
    return nuevo_progreso


# --------------------------------------------------------------
# Listar progresos (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.Progreso])
def obtener_progresos(db: Session = Depends(get_db)):
    """
    Devuelve todos los registros de progreso.
    """
    return db.query(models.Progreso).all()


# --------------------------------------------------------------
# Progreso por usuario (GET)
# --------------------------------------------------------------
@router.get("/usuario/{usuario_id}", response_model=list[schemas.Progreso])
def progreso_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Devuelve todo el progreso de un usuario específico.
    """
    progresos = db.query(models.Progreso).filter(models.Progreso.usuario_id == usuario_id).all()

    if not progresos:
        raise HTTPException(status_code=404, detail="No hay progreso registrado para este usuario")

    return progresos


# --------------------------------------------------------------
# Marcar reto como completado (PATCH / actualización parcial)
# --------------------------------------------------------------
@router.patch("/{progreso_id}", response_model=schemas.Progreso)
def completar_reto(progreso_id: int, db: Session = Depends(get_db)):
    """
    Marca un reto como completado.
    """

    progreso = db.query(models.Progreso).filter(models.Progreso.id == progreso_id).first()
    if not progreso:

        # --------------------------------------------------------------
        # Eliminar registro de progreso (DELETE)
        # --------------------------------------------------------------
        @router.delete("/{progreso_id}", status_code=status.HTTP_200_OK)
        def eliminar_registro(progreso_id: int, db: Session = Depends(get_db)):
            """
            Elimina un registro de progreso.
            """
            progreso = db.query(models.Progreso).filter(models.Progreso.id == progreso_id).first()
            if not progreso:
                raise HTTPException(status_code=404, detail="Registro no encontrado")

            db.delete(progreso)
            db.commit()
            return {"mensaje": f"Progreso con ID {progreso_id} eliminado correctamente."}

