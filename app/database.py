"""
Archivo: database.py
Descripción: Configura la conexión con la base de datos (SQLite)
Autor: Duván Guerrero
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Dirección de la base de datos (se guarda en un archivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./plataforma.db"

# Motor de conexión (permite conectarse a la base)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Sesión (permite ejecutar operaciones en la base)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de los modelos
Base = declarative_base()

# Función que maneja la conexión con la base
def get_db():
    """
    Crea una conexión a la base de datos y la cierra cuando se termina de usar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
