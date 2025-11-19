from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página de inicio que redirige según autenticación"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/home')
def home():
    """Página de inicio con contenido"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))
    return render_template('login.html')
