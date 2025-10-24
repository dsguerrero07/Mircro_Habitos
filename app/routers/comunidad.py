from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/comunidad",
    tags=["Comunidad"]
)

# --------------------------------------------------------------
# Crear comunidad (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Comunidad, status_code=status.HTTP_201_CREATED)
def crear_comunidad(data: schemas.ComunidadCreate, db: Session = Depends(get_db)):
    nueva_comunidad = models.Comunidad(
        nombre_reto=data.nombre_reto,
        categoria=data.categoria,
        duracion=data.duracion
    )

    db.add(nueva_comunidad)
    db.commit()
    db.refresh(nueva_comunidad)
    return nueva_comunidad


# --------------------------------------------------------------
# Listar comunidades (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.Comunidad])
def listar_comunidades(db: Session = Depends(get_db)):
    return db.query(models.Comunidad).all()


# --------------------------------------------------------------
# Obtener comunidad por ID (GET)
# --------------------------------------------------------------
@router.get("/{comunidad_id}", response_model=schemas.Comunidad)
def obtener_comunidad(comunidad_id: int, db: Session = Depends(get_db)):
    comunidad = db.query(models.Comunidad).filter(models.Comunidad.id == comunidad_id).first()
    if not comunidad:
        raise HTTPException(status_code=404, detail="Comunidad no encontrada")
    return comunidad


# --------------------------------------------------------------
# Ver participantes de una comunidad (GET)
# --------------------------------------------------------------
@router.get("/{comunidad_id}/participantes")
def obtener_participantes(comunidad_id: int, db: Session = Depends(get_db)):
    comunidad = db.query(models.Comunidad).filter(models.Comunidad.id == comunidad_id).first()
    if not comunidad:
        raise HTTPException(status_code=404, detail="Comunidad no encontrada")
    return comunidad.participantes


# --------------------------------------------------------------
# Agregar usuario a comunidad (POST)
# --------------------------------------------------------------
@router.post("/{comunidad_id}/agregar/{usuario_id}", status_code=status.HTTP_200_OK)
def agregar_usuario(comunidad_id: int, usuario_id: int, db: Session = Depends(get_db)):
    comunidad = db.query(models.Comunidad).filter(models.Comunidad.id == comunidad_id).first()
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    if not comunidad:
        raise HTTPException(status_code=404, detail="Comunidad no encontrada")
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Evitar duplicados
    if usuario in comunidad.participantes:
        raise HTTPException(status_code=400, detail="El usuario ya está en esta comunidad")

    comunidad.participantes.append(usuario)
    db.commit()
    return {"mensaje": f"Usuario {usuario_id} agregado a la comunidad {comunidad_id}."}


# --------------------------------------------------------------
# Remover usuario de comunidad (DELETE)
# --------------------------------------------------------------
@router.delete("/{comunidad_id}/remover/{usuario_id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(comunidad_id: int, usuario_id: int, db: Session = Depends(get_db)):
    comunidad = db.query(models.Comunidad).filter(models.Comunidad.id == comunidad_id).first()
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    if not comunidad:
        raise HTTPException(status_code=404, detail="Comunidad no encontrada")
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario not in comunidad.participantes:
        raise HTTPException(status_code=400, detail="El usuario no está en esta comunidad")

    comunidad.participantes.remove(usuario)
    db.commit()
    return {"mensaje": f"Usuario {usuario_id} eliminado de la comunidad {comunidad_id}."}


# --------------------------------------------------------------
# Eliminar comunidad por completo (DELETE)
# --------------------------------------------------------------
@router.delete("/{comunidad_id}")
def eliminar_comunidad(comunidad_id: int, db: Session = Depends(get_db)):
    comunidad = db.query(models.Comunidad).filter(models.Comunidad.id == comunidad_id).first()
    if not comunidad:
        raise HTTPException(status_code=404, detail="Comunidad no encontrada")

    db.delete(comunidad)
    db.commit()
    return {"mensaje": f"Comunidad {comunidad_id} eliminada correctamente."}
