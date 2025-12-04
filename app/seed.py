import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app import models

db = SessionLocal()

# ======================================
# USUARIOS EDUCATIVOS
# ======================================
usuarios = [
    models.Usuario(nombre="Ana Torres", edad=19, categoria="Estudiante", activo=True),
    models.Usuario(nombre="Carlos Ruiz", edad=22, categoria="Estudiante", activo=True),
    models.Usuario(nombre="Laura Gómez", edad=28, categoria="Docente", activo=True),
    models.Usuario(nombre="Pedro Martínez", edad=35, categoria="Instructor", activo=True),
    models.Usuario(nombre="Sofía Herrera", edad=20, categoria="Estudiante", activo=True),
]

# ======================================
# MICRORRETOS EDUCATIVOS
# ======================================
retos = [
    models.MicroReto(
        categoria="Python",
        dificultad="Baja",
        contenido="¿Qué es una variable en Python?",
        respuesta="Es un espacio en memoria para almacenar datos"
    ),
    models.MicroReto(
        categoria="Bases de Datos",
        dificultad="Media",
        contenido="¿Qué significa CRUD?",
        respuesta="Crear, Leer, Actualizar y Eliminar"
    ),
    models.MicroReto(
        categoria="FastAPI",
        dificultad="Media",
        contenido="¿Qué es un endpoint?",
        respuesta="Una ruta que responde a peticiones HTTP"
    ),
    models.MicroReto(
        categoria="Backend",
        dificultad="Alta",
        contenido="¿Qué es una API REST?",
        respuesta="Un servicio que permite consumir datos por HTTP"
    ),
]

db.add_all(usuarios)
db.add_all(retos)

db.commit()
db.close()

print("✅ Dataset educativo cargado correctamente")
