"""
Archivo: usuario.py
Descripción: Rutas (endpoints) para manejar usuarios en la plataforma.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

# Crear el router
router = APIRouter(
    prefix="/usuarios",          # La ruta base será /usuarios
    tags=["Usuarios"]            # Nombre del grupo en Swagger (docs)
)


# Dependencia: conexión con la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------------
#  Crear usuario (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.
    """
    # Verificar si ya existe un usuario con el mismo nombre
    existe = db.query(models.Usuario).filter(models.Usuario.nombre == usuario.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        edad=usuario.edad,
        categoria=usuario.categoria,
        nivel=usuario.nivel,
        racha_dias=usuario.racha_dias,
        puntos=usuario.puntos
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# --------------------------------------------------------------
#  Listar usuarios (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.Usuario])
def obtener_usuarios(db: Session = Depends(get_db)):
    """
    Devuelve la lista de todos los usuarios registrados.
    """
    usuarios = db.query(models.Usuario).all()
    return usuarios


# --------------------------------------------------------------
# Buscar usuario por ID (GET)
# --------------------------------------------------------------
@router.get("/{usuario_id}", response_model=schemas.Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Devuelve la información de un usuario específico según su ID.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# GET todas las gamificaciones de un usuario
@router.get("/{usuario_id}/gamificaciones", response_model=list[schemas.Gamificacion])
def obtener_gamificaciones_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.gamificaciones

# POST: crear gamificación para un usuario
@router.post("/{usuario_id}/gamificaciones", response_model=schemas.Gamificacion)
def crear_gamificacion_usuario(usuario_id: int, datos: schemas.GamificacionCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    nueva_gamificacion = models.Gamificacion(
        usuario_id=usuario.id,
        badge=datos.badge,
        puntos=datos.puntos
    )
    db.add(nueva_gamificacion)
    db.commit()
    db.refresh(nueva_gamificacion)
    return nueva_gamificacion


# GET todos los progresos de un usuario
@router.get("/{usuario_id}/progresos", response_model=list[schemas.Progreso])
def obtener_progresos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.progresos

# POST: crear progreso para un usuario
@router.post("/{usuario_id}/progresos", response_model=schemas.Progreso)
def crear_progreso_usuario(usuario_id: int, datos: schemas.ProgresoCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    nuevo_progreso = models.Progreso(
        usuario_id=usuario.id,
        reto_id=datos.reto_id,
        completado=datos.completado,
        fecha=datos.fecha
    )
    db.add(nuevo_progreso)
    db.commit()
    db.refresh(nuevo_progreso)
    return nuevo_progreso

# --------------------------------------------------------------
# Actualizar usuario (PUT)
# --------------------------------------------------------------
@router.put("/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(usuario_id: int, datos: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un usuario existente.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = datos.nombre
    usuario.edad = datos.edad
    usuario.categoria = datos.categoria
    usuario.nivel = datos.nivel
    usuario.racha_dias = datos.racha_dias
    usuario.puntos = datos.puntos

    db.commit()
    db.refresh(usuario)
    return usuario


# --------------------------------------------------------------
#  Eliminar usuario (DELETE)
# --------------------------------------------------------------
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos según su ID.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return None
