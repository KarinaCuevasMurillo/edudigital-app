import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def _normalizar_url_bd(url):
    if url and url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return url


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-de-respaldo-insegura'
    SQLALCHEMY_DATABASE_URI = _normalizar_url_bd(os.environ.get('DATABASE_URL')) or \
        'sqlite:///' + os.path.join(basedir, 'edudigital.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False