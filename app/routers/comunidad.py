from fastapi import APIRouter

router = APIRouter(
    prefix="/comunidad",
    tags=["Comunidad"]
)

"""
Archivo: comunidad.py
Descripción: Rutas (endpoints) para manejar las comunidades y retos grupales.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

# Crear el router
router = APIRouter(
    prefix="/comunidades",
    tags=["Comunidades"]
)

# Conexión con la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------------
# 1️⃣ Crear una comunidad (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Comunidad, status_code=status.HTTP_201_CREATED)
def crear_comunidad(comunidad: schemas.ComunidadCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva comunidad o reto grupal.
    """
    # Verificar si el usuario creador existe
    usuario = db.query(models.Usuario).filter(models.Usuario.id == comunidad.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nueva_comunidad = models.Comunidad(
        usuario_id=comunidad.usuario_id,
        nombre_reto=comunidad.nombre_reto,
        categoria=comunidad.categoria,
        duracion=comunidad.duracion,
        participantes=comunidad.participantes
    )

    db.add(nueva_comunidad)
    db.commit()
    db.refresh(nueva_comunidad)
    return nueva_comunidad


# --------------------------------------------------------------
# 2️⃣ Listar todas las comunidades (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.Comunidad])
def listar_comunidades(db: Session = Depends(get_db)):
    """
    Devuelve todas las comunidades creadas en la plataforma.
    """
    comunidades = db.query(models.Comunidad).all()
    return comunidades


# --------------------------------------------------------------
# 3️⃣ Obtener comunidad por ID (GET)
# --------------------------------------------------------------
@router.get("/{comunidad_id}", response_model=schemas.Comunidad)
def obtener_comunidad(comunidad_id: int, db: Session = Depends(get_db)):
    """
    Devuelve la información de una comunidad específica.
    """
    comunidad = db.query(models.Comunidad).filter(models.Comunidad.id == comunidad_id).first()
    if not comunidad:
        raise HTTPException(status_code=404, detail="Comunidad no encontrada")
    return comunidad


# --------------------------------------------------------------
# 4️⃣ Actualizar comunidad (PUT)
# --------------------------------------------------------------
@router.put("/{comunidad_id}", response_model=schemas.Comunidad)
def actualizar_comunidad(comunidad_id: int, datos: schemas.ComunidadCreate, db: Session = Depends(get_db)):
    """
    Actualiza la información de una comunidad existente.
    """
    comunidad = db.query(models.Comunidad).filter(models.Comunidad.id == comunidad_id).first()
    if not comunidad:
        raise HTTPException(status_code=404, detail="Comunidad no encontrada")

    comunidad.usuario_id = datos.usuario_id
    comunidad.nombre_reto = datos.nombre_reto
    comunidad.categoria = datos.categoria
    comunidad.duracion = datos.duracion
    comunidad.participantes = datos.participantes

    db.commit()
    db.refresh(comunidad)
    return comunidad


# --------------------------------------------------------------
# 5️⃣ Eliminar comunidad (DELETE)
# --------------------------------------------------------------
@router.delete("/{comunidad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_comunidad(comunidad_id: int, db: Session = Depends(get_db)):
    """
    Elimina una comunidad de la base de datos.
    """
    comunidad = db.query(models.Comunidad).filter(models.Comunidad.id == comunidad_id).first()
    if not comunidad:
        raise HTTPException(status_code=404, detail="Comunidad no encontrada")

    db.delete(comunidad)
    db.commit()
    return None
