from fastapi import APIRouter

router = APIRouter(
    prefix="/progreso",
    tags=["Progreso"],
)

"""
Archivo: progreso.py
Descripción: Rutas (endpoints) para manejar el progreso de los usuarios en los micro retos.
Autor: Duván Guerrero
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

# Crear el router
router = APIRouter(
    prefix="/progresos",
    tags=["Progresos"]
)

# Dependencia para la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------------
# 1️⃣ Crear un registro de progreso (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Progreso, status_code=status.HTTP_201_CREATED)
def crear_progreso(progreso: schemas.ProgresoCreate, db: Session = Depends(get_db)):
    """
    Registra el avance de un usuario en un micro reto.
    """
    # Verificamos si el usuario y el reto existen
    usuario = db.query(models.Usuario).filter(models.Usuario.id == progreso.usuario_id).first()
    reto = db.query(models.MicroReto).filter(models.MicroReto.id == progreso.reto_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
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
# 2️⃣ Listar todos los progresos (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.Progreso])
def listar_progresos(db: Session = Depends(get_db)):
    """
    Devuelve todos los registros de progreso de los usuarios.
    """
    progresos = db.query(models.Progreso).all()
    return progresos


# --------------------------------------------------------------
# 3️⃣ Obtener progreso por ID (GET)
# --------------------------------------------------------------
@router.get("/{progreso_id}", response_model=schemas.Progreso)
def obtener_progreso(progreso_id: int, db: Session = Depends(get_db)):
    """
    Devuelve un registro de progreso específico según su ID.
    """
    progreso = db.query(models.Progreso).filter(models.Progreso.id == progreso_id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso


# --------------------------------------------------------------
# 4️⃣ Actualizar un progreso (PUT)
# --------------------------------------------------------------
@router.put("/{progreso_id}", response_model=schemas.Progreso)
def actualizar_progreso(progreso_id: int, datos: schemas.ProgresoCreate, db: Session = Depends(get_db)):
    """
    Actualiza el registro de un progreso (por ejemplo, marcar un reto como completado).
    """
    progreso = db.query(models.Progreso).filter(models.Progreso.id == progreso_id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")

    progreso.usuario_id = datos.usuario_id
    progreso.reto_id = datos.reto_id
    progreso.completado = datos.completado
    progreso.fecha = datos.fecha

    db.commit()
    db.refresh(progreso)
    return progreso


# --------------------------------------------------------------
# 5️⃣ Eliminar un progreso (DELETE)
# --------------------------------------------------------------
@router.delete("/{progreso_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_progreso(progreso_id: int, db: Session = Depends(get_db)):
    """
    Elimina un registro de progreso de la base de datos.
    """
    progreso = db.query(models.Progreso).filter(models.Progreso.id == progreso_id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")

    db.delete(progreso)
    db.commit()
    return None
