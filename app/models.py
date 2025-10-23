"""
Archivo: models.py
Descripción: Define las tablas de la base de datos y sus relaciones
Autor: Duván Guerrero
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

# --------------------------------------------------------
# Tabla de Usuarios
# --------------------------------------------------------
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    edad = Column(Integer)
    categoria = Column(String)
    nivel = Column(String)
    racha_dias = Column(Integer, default=0)
    puntos = Column(Integer, default=0)

    # Relaciones con otras tablas
    progresos = relationship("Progreso", back_populates="usuario")
    gamificaciones = relationship("Gamificacion", back_populates="usuario")
    comunidades = relationship("Comunidad", back_populates="usuario")

# --------------------------------------------------------
# Tabla de MicroRetos
# --------------------------------------------------------
class MicroReto(Base):
    __tablename__ = "microretos"

    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String)
    dificultad = Column(String)
    contenido = Column(String)
    respuesta = Column(String)

    progresos = relationship("Progreso", back_populates="microrreto")

# --------------------------------------------------------
# Tabla de Progreso
# --------------------------------------------------------
class Progreso(Base):
    __tablename__ = "progresos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    reto_id = Column(Integer, ForeignKey("microretos.id"))
    completado = Column(String)
    fecha = Column(Date)

    usuario = relationship("Usuario", back_populates="progresos")
    microrreto = relationship("MicroReto", back_populates="progresos")

# --------------------------------------------------------
# Tabla de Gamificación
# --------------------------------------------------------
class Gamificacion(Base):
    __tablename__ = "gamificaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    badge = Column(String)
    puntos = Column(Integer)

    usuario = relationship("Usuario", back_populates="gamificaciones")

# --------------------------------------------------------
# Tabla de Comunidad
# --------------------------------------------------------
class Comunidad(Base):
    __tablename__ = "comunidades"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nombre_reto = Column(String)
    categoria = Column(String)
    duracion = Column(String)
    participantes = Column(Integer)

    usuario = relationship("Usuario", back_populates="comunidades")
