from fastapi import APIRouter

router = APIRouter(
    prefix="/microrretos",
    tags=["Microrretos"]
)

"""
Archivo: microrreto.py
Descripción: Rutas (endpoints) para manejar los micro retos educativos.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

# Crear el router
router = APIRouter(
    prefix="/microretos",        # Ruta base
    tags=["MicroRetos"]          # Sección en Swagger
)

# Conexión con la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------------
# 1️⃣ Crear un nuevo MicroReto (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.MicroReto, status_code=status.HTTP_201_CREATED)
def crear_microrreto(microrreto: schemas.MicroRetoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo micro reto educativo en la base de datos.
    """
    nuevo_reto = models.MicroReto(
        categoria=microrreto.categoria,
        dificultad=microrreto.dificultad,
        contenido=microrreto.contenido,
        respuesta=microrreto.respuesta
    )
    db.add(nuevo_reto)
    db.commit()
    db.refresh(nuevo_reto)
    return nuevo_reto


# --------------------------------------------------------------
# 2️⃣ Listar todos los MicroRetos (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.MicroReto])
def obtener_microretos(db: Session = Depends(get_db)):
    """
    Devuelve la lista de todos los micro retos registrados.
    """
    retos = db.query(models.MicroReto).all()
    return retos


# --------------------------------------------------------------
# 3️⃣ Obtener un MicroReto por ID (GET)
# --------------------------------------------------------------
@router.get("/{reto_id}", response_model=schemas.MicroReto)
def obtener_microrreto(reto_id: int, db: Session = Depends(get_db)):
    """
    Devuelve la información de un micro reto según su ID.
    """
    reto = db.query(models.MicroReto).filter(models.MicroReto.id == reto_id).first()
    if not reto:
        raise HTTPException(status_code=404, detail="MicroReto no encontrado")
    return reto


# --------------------------------------------------------------
# 4️⃣ Actualizar un MicroReto (PUT)
# --------------------------------------------------------------
@router.put("/{reto_id}", response_model=schemas.MicroReto)
def actualizar_microrreto(reto_id: int, datos: schemas.MicroRetoCreate, db: Session = Depends(get_db)):
    """
    Actualiza la información de un micro reto existente.
    """
    reto = db.query(models.MicroReto).filter(models.MicroReto.id == reto_id).first()
    if not reto:
        raise HTTPException(status_code=404, detail="MicroReto no encontrado")

    reto.categoria = datos.categoria
    reto.dificultad = datos.dificultad
    reto.contenido = datos.contenido
    reto.respuesta = datos.respuesta

    db.commit()
    db.refresh(reto)
    return reto


# --------------------------------------------------------------
# 5️⃣ Eliminar un MicroReto (DELETE)
# --------------------------------------------------------------
@router.delete("/{reto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_microrreto(reto_id: int, db: Session = Depends(get_db)):
    """
    Elimina un micro reto de la base de datos según su ID.
    """
    reto = db.query(models.MicroReto).filter(models.MicroReto.id == reto_id).first()
    if not reto:
        raise HTTPException(status_code=404, detail="MicroReto no encontrado")

    db.delete(reto)
    db.commit()
    return None

