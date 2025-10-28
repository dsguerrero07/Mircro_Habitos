"""
Archivo: database.py
Descripción: Configura la conexión con la base de datos (SQLite)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Dirección de la base de datos (se guarda en un archivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./plataforma.db"

# Motor de conexión (permite conectarse a la base)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Sesión (permite ejecutar operaciones en la base)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos
Base = declarative_base()

# Dependencia para usar DB en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
