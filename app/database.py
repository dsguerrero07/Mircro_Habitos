import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Leer la URL de la base de datos desde .env
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)

# Sesión (permite ejecutar operaciones en la BD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de modelos
Base = declarative_base()

# Dependencia para usar DB en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
