from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='config.Config'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config_name)
    
    # Crear directorio instance si no existe
    try:
        os.makedirs(os.path.join(app.config['BASE_DIR'], 'instance'), exist_ok=True)
    except OSError:
        pass
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    
    # Registrar blueprints - reordenado para que main.bp sea primero
    from app.main import main_bp
    from app.auth import auth_bp
    from app.notes import notes_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    return app
