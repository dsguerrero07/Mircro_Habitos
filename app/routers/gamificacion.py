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

# -------------------------------
# Modelos Pydantic de actualización
# -------------------------------
class GamificacionUpdateModel(schemas.BaseModel):
    usuario_id: int | None = None
    badge: str | None = None
    puntos: int | None = None

# --------------------------------------------------------------
# 1️⃣ Crear una recompensa o insignia (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Gamificacion, status_code=status.HTTP_201_CREATED)
def crear_gamificacion(gamificacion: schemas.GamificacionCreate, db: Session = Depends(get_db)):
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
    return db.query(models.Gamificacion).all()

# --------------------------------------------------------------
# 3️⃣ Obtener gamificación por ID (GET)
# --------------------------------------------------------------
@router.get("/{gamificacion_id}", response_model=schemas.Gamificacion)
def obtener_gamificacion(gamificacion_id: int, db: Session = Depends(get_db)):
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.id == gamificacion_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Registro de gamificación no encontrado")
    return gamificacion

# --------------------------------------------------------------
# 4️⃣ Actualizar gamificación (PUT)
# --------------------------------------------------------------
@router.put("/{gamificacion_id}", response_model=schemas.Gamificacion)
def actualizar_gamificacion(gamificacion_id: int, datos: GamificacionUpdateModel, db: Session = Depends(get_db)):
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.id == gamificacion_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Registro de gamificación no encontrado")

    # Actualizar solo los campos enviados
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(gamificacion, key, value)

    db.commit()
    db.refresh(gamificacion)
    return gamificacion

# --------------------------------------------------------------
# 5️⃣ Eliminar gamificación (DELETE)
# --------------------------------------------------------------
@router.delete("/{gamificacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_gamificacion(gamificacion_id: int, db: Session = Depends(get_db)):
    gamificacion = db.query(models.Gamificacion).filter(models.Gamificacion.id == gamificacion_id).first()
    if not gamificacion:
        raise HTTPException(status_code=404, detail="Registro de gamificación no encontrado")
    db.delete(gamificacion)
    db.commit()
    return None

