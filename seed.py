from app import create_app
from app.seed_data import cargar_datos_ejemplo

# create_app() ya carga los datos de ejemplo si la base está vacía.
# Este script queda por si quieres forzar la carga manualmente: python seed.py
app = create_app()
with app.app_context():
    cargar_datos_ejemplo()
