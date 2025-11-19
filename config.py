import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    # Directorio base
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Configuración de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "notes.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-muy-segura-cambia-esto'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    
    # Configuración de seguridad
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    REMEMBER_COOKIE_HTTPONLY = True
