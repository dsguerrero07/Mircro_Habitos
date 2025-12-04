from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
import os
import shutil

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

templates = Jinja2Templates(directory="app/templates")

# ==========================================================
#  VISTA HTML: LISTADO DE USUARIOS
# ==========================================================
@router.get("/vista")
def vista_usuarios(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).filter(models.Usuario.activo == True).all()
    return templates.TemplateResponse(
        "usuarios.html",
        {"request": request, "usuarios": usuarios}
    )

# ==========================================================
#  FORMULARIO HTML
# ==========================================================
@router.get("/nuevo")
def formulario_usuario(request: Request):
    return templates.TemplateResponse(
        "crear_usuario.html",
        {"request": request}
    )

# ==========================================================
#  POST DESDE FORMULARIO HTML (CORREGIDO)
# ==========================================================
@router.post("/crear-html")
def crear_usuario_html(
    nombre: str = Form(...),
    edad: int = Form(...),
    categoria: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    existe = db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    ruta_foto = None

    if foto:
        carpeta = "app/static/uploads"
        os.makedirs(carpeta, exist_ok=True)

        ruta_foto = f"{carpeta}/{foto.filename}"
        with open(ruta_foto, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

        ruta_foto = f"/static/uploads/{foto.filename}"

    nuevo_usuario = models.Usuario(
        nombre=nombre,
        edad=edad,
        categoria=categoria,
        foto=ruta_foto,
        activo=True
    )

    db.add(nuevo_usuario)
    db.commit()

    return RedirectResponse("/usuarios/vista", status_code=303)
# ==========================================================
#  API ORIGINAL (NO SE TOCA)
# ==========================================================

@router.post("/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.nombre == usuario.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo_usuario = models.Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.get("/", response_model=list[schemas.Usuario])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).filter(models.Usuario.activo == True).all()


@router.get("/eliminados", response_model=list[schemas.Usuario])
def usuarios_eliminados(db: Session = Depends(get_db)):
    return db.query(models.Usuario).filter(models.Usuario.activo == False).all()


@router.get("/{usuario_id}", response_model=schemas.Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.get("/buscar/{nombre}", response_model=schemas.Usuario)
def buscar_usuario_por_nombre(nombre: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.nombre == nombre, models.Usuario.activo == True).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No existe un usuario activo con ese nombre")
    return usuario


@router.put("/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(usuario_id: int, datos: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for campo, valor in datos.model_dump().items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.activo = False
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}


@router.put("/restaurar/{usuario_id}", response_model=schemas.Usuario)
def restaurar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.activo = True
    db.commit()
    db.refresh(usuario)
    return usuario
