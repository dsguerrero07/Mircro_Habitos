"""
Archivo: schemas.py
Descripción: Modelos de validación de datos (entrada y salida)

"""
from pydantic import BaseModel
from datetime import datetime

# --------------------------------------------------------
# Usuario
# --------------------------------------------------------
class UsuarioBase(BaseModel):
    nombre: str
    edad: int
    categoria: str
    nivel: int = 1
    racha_dias: int = 0
    puntos: int = 0

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    class Config:
        from_attributes = True


# --------------------------------------------------------
# MicroReto
# --------------------------------------------------------
class MicroRetoBase(BaseModel):
    categoria: str
    dificultad: str
    contenido: str
    respuesta: str

class MicroRetoCreate(MicroRetoBase):
    pass

class MicroReto(MicroRetoBase):
    id: int
    class Config:
        from_attributes = True


# --------------------------------------------------------
# Progreso
# --------------------------------------------------------
class ProgresoBase(BaseModel):
    usuario_id: int
    reto_id: int
    completado: bool = False
    fecha: datetime = datetime.utcnow()

class ProgresoCreate(ProgresoBase):
    pass

class Progreso(ProgresoBase):
    id: int
    class Config:
        from_attributes = True


# --------------------------------------------------------
# Gamificación
# --------------------------------------------------------
class GamificacionBase(BaseModel):
    usuario_id: int
    badge: str = "Ninguno"
    puntos: int = 0

class GamificacionCreate(GamificacionBase):
    pass

class Gamificacion(GamificacionBase):
    id: int
    class Config:
        from_attributes = True


# --------------------------------------------------------
# Comunidad
# --------------------------------------------------------
class ComunidadBase(BaseModel):
    nombre_reto: str
    categoria: str
    duracion: int  # Días o semanas

class ComunidadCreate(ComunidadBase):
    pass

class Comunidad(ComunidadBase):
    id: int
    class Config:
        from_attributes = True

