from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# --------------------------------------------------------------
#  Crear usuario (POST)
# --------------------------------------------------------------
@router.post("/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos si el nombre no está repetido.
    """
    existe = db.query(models.Usuario).filter(models.Usuario.nombre == usuario.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo_usuario = models.Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# --------------------------------------------------------------
#  Listar usuarios activos (GET)
# --------------------------------------------------------------
@router.get("/", response_model=list[schemas.Usuario])
def obtener_usuarios(db: Session = Depends(get_db)):
    """
    Retorna todos los usuarios con estado activo = True.
    """
    return db.query(models.Usuario).filter(models.Usuario.activo == True).all()


# --------------------------------------------------------------
#  Listar usuarios eliminados (GET)
# --------------------------------------------------------------
@router.get("/eliminados", response_model=list[schemas.Usuario])
def usuarios_eliminados(db: Session = Depends(get_db)):
    """
    Retorna todos los usuarios con estado activo = False (eliminados lógicamente).
    """
    return db.query(models.Usuario).filter(models.Usuario.activo == False).all()


# --------------------------------------------------------------
# Buscar usuario por ID (GET)
# --------------------------------------------------------------
@router.get("/{usuario_id}", response_model=schemas.Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Busca y retorna un usuario por su ID.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# --------------------------------------------------------------
# Buscar usuario por nombre (GET)
# --------------------------------------------------------------
@router.get("/buscar/{nombre}", response_model=schemas.Usuario)
def buscar_usuario_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """
    Busca un usuario por su nombre exacto.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.nombre == nombre, models.Usuario.activo == True).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="No existe un usuario activo con ese nombre")

    return usuario

# --------------------------------------------------------------
# Actualizar usuario (PUT)
# --------------------------------------------------------------
@router.put("/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(usuario_id: int, datos: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Actualiza todos los campos de un usuario existente.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for campo, valor in datos.model_dump().items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario


# --------------------------------------------------------------
# Eliminar usuario (DELETE) - eliminación lógica
# --------------------------------------------------------------
@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Marca un usuario como inactivo (activo = False) en lugar de eliminarlo físicamente.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.activo = False
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}


# --------------------------------------------------------------
# Restaurar usuario (PUT)
# --------------------------------------------------------------
@router.put("/restaurar/{usuario_id}", response_model=schemas.Usuario)
def restaurar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Restaura un usuario previamente eliminado (activo = False).
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.activo = True
    db.commit()
    db.refresh(usuario)

    return usuario
