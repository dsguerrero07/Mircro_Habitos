from fastapi import APIRouter

router = APIRouter(
    prefix="/gamificacion",
    tags=["Gamificacion"],
)

"""
Archivo: gamificacion.py
Descripción: Rutas (endpoints) para manejar el sistema de puntos e insignias de los usuarios.
Autor: Duván Guerrero
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

# Crear el router
router = APIRouter(
    prefix="/gamificacion",
    tags=["Gamificación"]
)

# Conexión con la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------------
# 1️⃣ Crear una recompensa o insignia (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Gamificacion, status_code=status.HTTP_201_CREATED)
def crear_gamificacion(gamificacion: schemas.GamificacionCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo registro de gamificación (puntos o insignias) para un usuario.
    """
    # Verificamos si el usuario existe
    usuario = db.query(models.Usuario).filter(models.Usuario.id == gamificacion.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nueva_gamificacion = models.Gamificacion(
        usuario_id=gamificacion.usuario_id,
        badge=gamificacion.badge,
        puntos=gamificacion.puntos
    )

    db.add(nueva_gamificacion)
    db.commit()
    db.refresh(nueva_gamificacion)
    return nueva_gamificacion


# --------------------------------------------------------------
# 2️⃣ Listar todas las recompensas (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.Gamificacion])
def listar_gamificaciones(db: Session = Depends(get_db)):
    """
    Devuelve todas las insignias y puntos registrados.
    """
    gamificaciones = db.query(models.Gamificacion).all()
    return gamificaciones


# --------------------------------------------------------------
# 3️⃣ Obtener gamificación por ID (GET)
# --------------------------------------------------------------
@router.get("/{gamificacion_id}", response_model=schemas.Gamificacion)
def obtener_gamificacion(gamificacion_id: int, db: Session = Depends(get_db)):
    """
    Devuelve una gamificación específica según su ID.
    """
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.id == gamificacion_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Registro de gamificación no encontrado")
    return gamificacion


# --------------------------------------------------------------
# 4️⃣ Actualizar gamificación (PUT)
# --------------------------------------------------------------
@router.put("/{gamificacion_id}", response_model=schemas.Gamificacion)
def actualizar_gamificacion(gamificacion_id: int, datos: schemas.GamificacionCreate, db: Session = Depends(get_db)):
    """
    Actualiza una recompensa o puntaje de un usuario.
    """
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.id == gamificacion_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Registro de gamificación no encontrado")

    gamificacion.usuario_id = datos.usuario_id
    gamificacion.badge = datos.badge
    gamificacion.puntos = datos.puntos

    db.commit()
    db.re
