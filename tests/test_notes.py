import unittest
from app import create_app, db
from app.models import User, Note

class TestNotesRoutes(unittest.TestCase):
    """Pruebas unitarias para las rutas de notas"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Crear y autenticar usuario de prueba
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()
        
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
    
    def tearDown(self):
        """Limpieza después de cada test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_dashboard_requires_login(self):
        """Test: El dashboard requiere autenticación"""
        self.client.get('/logout')
        response = self.client.get('/notes/dashboard')
        self.assertEqual(response.status_code, 302)
    
    def test_create_note_success(self):
        """Test: Crear una nota exitosamente"""
        response = self.client.post('/notes/create', data={
            'title': 'Test Note',
            'content': 'This is test content'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        note = Note.query.filter_by(title='Test Note').first()
        self.assertIsNotNone(note)
        self.assertEqual(note.content, 'This is test content')
        self.assertEqual(note.user_id, self.user.id)
    
    def test_create_note_without_title(self):
        """Test: No se puede crear nota sin título"""
        response = self.client.post('/notes/create', data={
            'title': '',
            'content': 'Content without title'
        }, follow_redirects=True)
        
        self.assertIn(b'obligatorio', response.data)
    
    def test_create_note_without_content(self):
        """Test: No se puede crear nota sin contenido"""
        response = self.client.post('/notes/create', data={
            'title': 'Title',
            'content': ''
        }, follow_redirects=True)
        
        self.assertIn(b'obligatorio', response.data)
    
    def test_view_note_success(self):
        """Test: Ver una nota existente"""
        note = Note(
            title='Test Note',
            content='Test Content',
            user_id=self.user.id
        )
        db.session.add(note)
        db.session.commit()
        
        response = self.client.get(f'/notes/{note.id}')
        self.assertEqual(response.status_code, 200)
    
    def test_view_note_unauthorized(self):
        """Test: No se puede ver nota de otro usuario"""
        other_user = User(username='otheruser', email='other@example.com')
        other_user.set_password('password123')
        db.session.add(other_user)
        db.session.commit()
        
        note = Note(
            title='Other User Note',
            content='Content',
            user_id=other_user.id
        )
        db.session.add(note)
        db.session.commit()
        
        response = self.client.get(f'/notes/{note.id}', follow_redirects=True)
        self.assertIn(b'permiso', response.data)
    
    def test_edit_note_success(self):
        """Test: Editar una nota exitosamente"""
        note = Note(
            title='Original Title',
            content='Original Content',
            user_id=self.user.id
        )
        db.session.add(note)
        db.session.commit()
        
        response = self.client.post(f'/notes/{note.id}/edit', data={
            'title': 'Updated Title',
            'content': 'Updated Content'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        updated_note = Note.query.get(note.id)
        self.assertEqual(updated_note.title, 'Updated Title')
        self.assertEqual(updated_note.content, 'Updated Content')
    
    def test_delete_note_success(self):
        """Test: Eliminar una nota exitosamente"""
        note = Note(
            title='Note to Delete',
            content='Content',
            user_id=self.user.id
        )
        db.session.add(note)
        db.session.commit()
        note_id = note.id
        
        response = self.client.post(f'/notes/{note_id}/delete', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Note.query.get(note_id))
    
    def test_toggle_complete_success(self):
        """Test: Marcar/desmarcar nota como completada"""
        note = Note(
            title='Test Note',
            content='Content',
            user_id=self.user.id,
            is_completed=False
        )
        db.session.add(note)
        db.session.commit()
        
        response = self.client.post(f'/notes/{note.id}/toggle-complete')
        self.assertEqual(response.status_code, 200)
        
        updated_note = Note.query.get(note.id)
        self.assertTrue(updated_note.is_completed)


if __name__ == '__main__':
    unittest.main()