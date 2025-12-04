"""
Archivo: models.py
Descripción: Define las tablas de la base de datos y sus relaciones

"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
# --------------------------------------------------------
# Tabla de Usuarios
# --------------------------------------------------------
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer)
    categoria = Column(String)
    nivel = Column(Integer, default=1)
    racha_dias = Column(Integer, default=0)
    puntos = Column(Integer, default=0)

    foto = Column(String, nullable=False)

    activo = Column(Boolean, default=True)

    # Relaciones
    progreso = relationship("Progreso", back_populates="usuario")
    gamificacion = relationship("Gamificacion", back_populates="usuario", uselist=False)
    comunidades = relationship("Comunidad", secondary="usuarios_comunidad", back_populates="participantes")


class MicroReto(Base):
    __tablename__ = "microrretos"

    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String)
    dificultad = Column(String)
    contenido = Column(String)
    respuesta = Column(String)

    progreso = relationship("Progreso", back_populates="reto")


class Progreso(Base):
    __tablename__ = "progreso"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    reto_id = Column(Integer, ForeignKey("microrretos.id"))
    completado = Column(Boolean, default=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="progreso")
    reto = relationship("MicroReto", back_populates="progreso")


class Gamificacion(Base):
    __tablename__ = "gamificacion"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    badge = Column(String, default="Ninguno")
    puntos = Column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="gamificacion")


class Comunidad(Base):
    __tablename__ = "comunidades"

    id = Column(Integer, primary_key=True, index=True)
    nombre_reto = Column(String)
    categoria = Column(String)
    duracion = Column(Integer)

    participantes = relationship("Usuario", secondary="usuarios_comunidad", back_populates="comunidades")


# Tabla intermedia N:M para comunidad
from sqlalchemy import Table, MetaData

usuarios_comunidad = Table(
    "usuarios_comunidad",
    Base.metadata,
    Column("usuario_id", Integer, ForeignKey("usuarios.id")),
    Column("comunidad_id", Integer, ForeignKey("comunidades.id"))
)
