# EduDigital

Plataforma web de aprendizaje adaptativo con diagnóstico inicial, quizzes por tema, panel docente, encuesta de uso y exportación de resultados a CSV. Proyecto "Educación en la Era Digital", Taller de Investigación II, Tec Tijuana (2026).

Demo: https://edudigital-app.onrender.com

## Ejecutar en local

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python run.py

Abre http://127.0.0.1:5000. Si la base está vacía, la app carga sola los datos de ejemplo. `python seed.py` solo sirve para forzar esa carga.

## Variables de entorno (opcionales)

Se leen desde el entorno o desde un archivo `.env` en la raíz:

- SECRET_KEY: clave de sesión. Defínela en producción.
- DATABASE_URL: base PostgreSQL. Si no existe, se usa SQLite (edudigital.db).
- DOCENTE_CODIGO: código para registrarse como docente. Defínelo en producción.

## Estructura

- app/models.py: modelos de base de datos
- app/routes/: rutas de autenticación, estudiante y docente
- app/seed_data.py, app/seed_extra.py: banco de preguntas y datos de ejemplo
- app/templates/ y app/static/: vistas y estilos
- config.py, run.py, seed.py: configuración y arranque

## Equipo

Karina Sarahi Cuevas Murillo, Steven Daniel Guzman Orozco, Fidel Muñoz Martinez.
