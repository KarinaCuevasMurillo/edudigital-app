import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def _normalizar_url_bd(url):
    if url and url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return url


if not os.environ.get('SECRET_KEY'):
    print('AVISO: define la variable SECRET_KEY en producción (se está usando una clave de respaldo).')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-de-respaldo-insegura'
    SQLALCHEMY_DATABASE_URI = _normalizar_url_bd(os.environ.get('DATABASE_URL')) or \
        'sqlite:///' + os.path.join(basedir, 'edudigital.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Código que debe escribir quien se registre como docente (cámbialo en Render con la variable DOCENTE_CODIGO)
    DOCENTE_CODIGO = os.environ.get('DOCENTE_CODIGO') or 'DOCENTE2026'