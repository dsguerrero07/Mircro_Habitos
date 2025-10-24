# MicroHábitos - Proyecto Integrador

## Descripción
MicroHábitos es una aplicación que permite a los usuarios crear y cumplir microretos diarios, acumular puntos y obtener insignias mediante un sistema de gamificación, y participar en comunidades para fomentar hábitos positivos. La aplicación gestiona el progreso de los usuarios, sus recompensas y la interacción con otros miembros, proporcionando un sistema motivacional completo.

## Objetivo
El objetivo del proyecto es exponer una experiencia de desarrollo integral, demostrando la interacción de modelos y la aplicación de reglas de negocio para generar un sistema funcional de hábitos y gamificación. Además, se busca recibir retroalimentación que permita mejorar la ejecución y la lógica del proyecto.

## Tecnologías utilizadas
- **Python 3.13**
- **FastAPI** (framework web para APIs)
- **SQLAlchemy** (ORM para manejo de bases de datos)
- **SQLite / PostgreSQL** (motor de base de datos)
- **Pydantic** (validación de datos)
- **Swagger / OpenAPI** (documentación de la API)
- **Pandas / openpyxl** (para generación de reportes XLSX)
- **Uvicorn** (servidor ASGI)

- ## Mapa de  Endpoints
- POST /usuarios/
{
  "nombre": "Duvan",
  "edad": 22,
  "categoria": "Avanzado",
  "nivel": "Intermedio",
  "racha_dias": 3,
  "puntos": 100
}

GET /usuarios/
GET /usuarios/{usuario_id}

PUT /usuarios/{usuario_id}
{
  "nombre": "Duvan Actualizado",
  "edad": 23,
  "categoria": "Avanzado",
  "nivel": "Avanzado",
  "racha_dias": 4,
  "puntos": 120
}

DELETE /usuarios/{usuario_id}

POST /microretos/
{
  "categoria": "Salud",
  "dificultad": "Media",
  "contenido": "Hacer 10 flexiones",
  "respuesta": "Completado"
}

GET /microretos/
GET /microretos/{microreto_id}

PUT /microretos/{microreto_id}
{
  "categoria": "Salud",
  "dificultad": "Alta",
  "contenido": "Hacer 20 flexiones",
  "respuesta": "Completado"
}

DELETE /microretos/{microreto_id}

POST /gamificacion/
{
  "usuario_id": 1,
  "badge": "Iniciador",
  "puntos": 50
}

GET /gamificacion/
GET /gamificacion/{gamificacion_id}

PUT /gamificacion/{gamificacion_id}
{
  "usuario_id": 1,
  "badge": "Experto",
  "puntos": 100
}

POST /progreso/
{
  "usuario_id": 1,
  "reto_id": 2,
  "completado": "Sí",
  "fecha": "2025-10-23"
}

GET /progreso/
GET /progreso/{progreso_id}

PUT /progreso/{progreso_id}
{
  "usuario_id": 1,
  "reto_id": 2,
  "completado": "Sí",
  "fecha": "2025-10-24"
}

POST /comunidades/
{
  "usuario_id": 1,
  "nombre_reto": "Reto Saludable",
  "categoria": "Salud",
  "duracion": "30 días",
  "participantes": 10
}

GET /comunidades/
GET /comunidades/{comunidad_id}

PUT /comunidades/{comunidad_id}
{
  "usuario_id": 1,
  "nombre_reto": "Reto Saludable Avanzado",
  "categoria": "Salud",
  "duracion": "45 días",
  "participantes": 12
}


## Instalación y ejecución
1. Clonar el repositorio:
```bash
git clone https://github.com/dsguerrero07/Mircro_Habitos.git
