from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/microrretos",
    tags=["MicroRetos"]
)

# --------------------------------------------------------------
# Crear Microrreto (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.MicroReto, status_code=status.HTTP_201_CREATED)
def crear_microrreto(reto: schemas.MicroRetoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo MicroReto.
    """
    nuevo_reto = models.MicroReto(
        categoria=reto.categoria,
        dificultad=reto.dificultad,
        contenido=reto.contenido,
        respuesta=reto.respuesta
    )

    db.add(nuevo_reto)
    db.commit()
    db.refresh(nuevo_reto)
    return nuevo_reto


# --------------------------------------------------------------
# Listar Microrretos (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.MicroReto])
def listar_microrretos(db: Session = Depends(get_db)):
    """
    Devuelve la lista de todos los Microrretos.
    """
    return db.query(models.MicroReto).all()


# --------------------------------------------------------------
# Obtener Microrreto por ID (GET)
# --------------------------------------------------------------
@router.get("/{microrreto_id}", response_model=schemas.MicroReto)
def obtener_microrreto(microrreto_id: int, db: Session = Depends(get_db)):
    """
    Devuelve un Microrreto específico.
    """
    reto = db.query(models.MicroReto).filter(models.MicroReto.id == microrreto_id).first()
    if not reto:
        raise HTTPException(status_code=404, detail="MicroReto no encontrado")
    return reto


# --------------------------------------------------------------
# Actualizar Microrreto (PUT)
# --------------------------------------------------------------
@router.put("/{microrreto_id}", response_model=schemas.MicroReto)
def actualizar_microrreto(microrreto_id: int, datos: schemas.MicroRetoCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un Microrreto existente.
    """
    reto = db.query(models.MicroReto).filter(models.MicroReto.id == microrreto_id).first()
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
# Eliminar Microrreto (DELETE)
# --------------------------------------------------------------
@router.delete("/{microrreto_id}", status_code=status.HTTP_200_OK)
def eliminar_microrreto(microrreto_id: int, db: Session = Depends(get_db)):
    """
    Elimina un Microrreto de la base de datos.
    """
    reto = db.query(models.MicroReto).filter(models.MicroReto.id == microrreto_id).first()
    if not reto:
        raise HTTPException(status_code=404, detail="MicroReto no encontrado")

    db.delete(reto)
    db.commit()
    return {"mensaje": f"MicroReto con ID {microrreto_id} eliminado correctamente."}
