from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevo usuario"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validaciones
        if not username or not email or not password:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('auth.register'))
        
        if len(username) < 3:
            flash('El nombre de usuario debe tener al menos 3 caracteres.', 'error')
            return redirect(url_for('auth.register'))
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return redirect(url_for('auth.register'))
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado.', 'error')
            return redirect(url_for('auth.register'))
        
        # Crear nuevo usuario
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registro exitoso. Por favor, inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Usuario y contraseña son obligatorios.', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Usuario o contraseña incorrectos.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        flash(f'Bienvenido, {user.username}!', 'success')
        return redirect(url_for('notes.dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Cierre de sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/')
def index():
    """Página de inicio que redirige según autenticación"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))
    return redirect(url_for('auth.login'))
