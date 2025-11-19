from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Note

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

@notes_bp.route('/dashboard')
@login_required
def dashboard():
    """Panel de control con todas las notas del usuario"""
    page = request.args.get('page', 1, type=int)
    notes = Note.query.filter_by(user_id=current_user.id).order_by(
        Note.updated_at.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('dashboard.html', notes=notes)


@notes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    """Crear una nueva nota"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        
        if not title:
            flash('El título es obligatorio.', 'error')
            return redirect(url_for('notes.create_note'))
        
        if not content:
            flash('El contenido es obligatorio.', 'error')
            return redirect(url_for('notes.create_note'))
        
        note = Note(title=title, content=content, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        
        flash('Nota creada exitosamente.', 'success')
        return redirect(url_for('notes.dashboard'))
    
    return render_template('create_note.html')


@notes_bp.route('/<int:note_id>')
@login_required
def view_note(note_id):
    """Ver una nota específica"""
    note = Note.query.get_or_404(note_id)
    
    # Verificar que la nota pertenece al usuario actual
    if note.user_id != current_user.id:
        flash('No tienes permiso para acceder a esta nota.', 'error')
        return redirect(url_for('notes.dashboard'))
    
    return render_template('view_note.html', note=note)


@notes_bp.route('/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    """Editar una nota existente"""
    note = Note.query.get_or_404(note_id)
    
    # Verificar que la nota pertenece al usuario actual
    if note.user_id != current_user.id:
        flash('No tienes permiso para editar esta nota.', 'error')
        return redirect(url_for('notes.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        
        if not title:
            flash('El título es obligatorio.', 'error')
            return redirect(url_for('notes.edit_note', note_id=note_id))
        
        if not content:
            flash('El contenido es obligatorio.', 'error')
            return redirect(url_for('notes.edit_note', note_id=note_id))
        
        note.title = title
        note.content = content
        db.session.commit()
        
        flash('Nota actualizada exitosamente.', 'success')
        return redirect(url_for('notes.dashboard'))
    
    return render_template('edit_note.html', note=note)


@notes_bp.route('/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    """Eliminar una nota"""
    note = Note.query.get_or_404(note_id)
    
    # Verificar que la nota pertenece al usuario actual
    if note.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta nota.', 'error')
        return redirect(url_for('notes.dashboard'))
    
    db.session.delete(note)
    db.session.commit()
    
    flash('Nota eliminada exitosamente.', 'success')
    return redirect(url_for('notes.dashboard'))


@notes_bp.route('/<int:note_id>/toggle-complete', methods=['POST'])
@login_required
def toggle_complete(note_id):
    """Marcar/desmarcar una nota como completada"""
    note = Note.query.get_or_404(note_id)
    
    # Verificar que la nota pertenece al usuario actual
    if note.user_id != current_user.id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    note.is_completed = not note.is_completed
    db.session.commit()
    
    return jsonify({'success': True, 'is_completed': note.is_completed})