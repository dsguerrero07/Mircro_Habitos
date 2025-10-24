from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/gamificacion",
    tags=["Gamificación"]
)

# --------------------------------------------------------------
# Crear registro de gamificación para un usuario (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Gamificacion, status_code=status.HTTP_201_CREATED)
def crear_gamificacion(data: schemas.GamificacionCreate, db: Session = Depends(get_db)):
    """
    Crea o asigna un sistema de puntos y logros a un usuario.
    """

    # Validar que el usuario exista
    usuario = db.query(models.Usuario).filter(models.Usuario.id == data.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si ya tiene gamificación asignada
    existe = db.query(models.Gamificacion).filter(models.Gamificacion.usuario_id == data.usuario_id).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este usuario ya tiene gamificación registrada")

    nuevo = models.Gamificacion(
        usuario_id=data.usuario_id,
        badge=data.badge,
        puntos=data.puntos
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# --------------------------------------------------------------
# Ver gamificación de todos los usuarios (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.Gamificacion])
def obtener_gamificaciones(db: Session = Depends(get_db)):
    return db.query(models.Gamificacion).all()


# --------------------------------------------------------------
# Ver gamificación de un usuario específico (GET)
# --------------------------------------------------------------
@router.get("/{usuario_id}", response_model=schemas.Gamificacion)
def obtener_gamificacion(usuario_id: int, db: Session = Depends(get_db)):
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.usuario_id == usuario_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Este usuario no tiene gamificación registrada")
    return gamificacion


# --------------------------------------------------------------
# Añadir puntos a un usuario (PATCH)
# --------------------------------------------------------------
@router.patch("/{usuario_id}/sumar-puntos", response_model=schemas.Gamificacion)
def sumar_puntos(usuario_id: int, puntos: int, db: Session = Depends(get_db)):
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.usuario_id == usuario_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Gamificación no encontrada")

    gamificacion.puntos += puntos
    db.commit()
    db.refresh(gamificacion)
    return gamificacion


# --------------------------------------------------------------
# Cambiar badge (PATCH)
# --------------------------------------------------------------
@router.patch("/{usuario_id}/cambiar-badge", response_model=schemas.Gamificacion)
def cambiar_badge(usuario_id: int, badge: str, db: Session = Depends(get_db)):
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.usuario_id == usuario_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Gamificación no encontrada")

    gamificacion.badge = badge
    db.commit()
    db.refresh(gamificacion)
    return gamificacion


# --------------------------------------------------------------
# Eliminar registro de gamificación (DELETE)
# --------------------------------------------------------------
@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def eliminar_gamificacion(usuario_id: int, db: Session = Depends(get_db)):
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.usuario_id == usuario_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Gamificación no encontrada")

    db.delete(gamificacion)
    db.commit()
    return {"mensaje": f"Registro de gamificación del usuario {usuario_id} eliminado correctamente."}
