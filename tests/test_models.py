import unittest
from app import create_app, db
from app.models import User, Note
from datetime import datetime

class TestUserModel(unittest.TestCase):
    """Pruebas unitarias para el modelo User"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password_hashing(self):
        """Test: Las contraseñas se encriptan correctamente"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        
        self.assertNotEqual(user.password_hash, 'password123')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_user_creation(self):
        """Test: Se puede crear un usuario correctamente"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertTrue(retrieved_user.check_password('password123'))
    
    def test_unique_username(self):
        """Test: Los nombres de usuario deben ser únicos"""
        user1 = User(username='testuser', email='test1@example.com')
        user1.set_password('password123')
        db.session.add(user1)
        db.session.commit()
        
        user2 = User(username='testuser', email='test2@example.com')
        user2.set_password('password456')
        db.session.add(user2)
        
        with self.assertRaises(Exception):
            db.session.commit()
    
    def test_user_repr(self):
        """Test: La representación del usuario es correcta"""
        user = User(username='testuser', email='test@example.com')
        self.assertEqual(repr(user), '<User testuser>')


class TestNoteModel(unittest.TestCase):
    """Pruebas unitarias para el modelo Note"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Crear usuario de prueba
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_note_creation(self):
        """Test: Se puede crear una nota correctamente"""
        note = Note(
            title='Test Note',
            content='This is a test note',
            user_id=self.user.id
        )
        db.session.add(note)
        db.session.commit()
        
        retrieved_note = Note.query.first()
        self.assertIsNotNone(retrieved_note)
        self.assertEqual(retrieved_note.title, 'Test Note')
        self.assertEqual(retrieved_note.content, 'This is a test note')
        self.assertEqual(retrieved_note.user_id, self.user.id)
    
    def test_note_default_values(self):
        """Test: Los valores por defecto de las notas son correctos"""
        note = Note(
            title='Test Note',
            content='Content',
            user_id=self.user.id
        )
        db.session.add(note)
        db.session.commit()
        
        self.assertFalse(note.is_completed)
        self.assertIsInstance(note.created_at, datetime)
        self.assertIsInstance(note.updated_at, datetime)
    
    def test_note_user_relationship(self):
        """Test: La relación entre nota y usuario funciona"""
        note = Note(
            title='Test Note',
            content='Content',
            user_id=self.user.id
        )
        db.session.add(note)
        db.session.commit()
        
        self.assertEqual(note.author.username, 'testuser')
        self.assertIn(note, self.user.notes)
    
    def test_note_completion_toggle(self):
        """Test: Se puede marcar una nota como completada"""
        note = Note(
            title='Test Note',
            content='Content',
            user_id=self.user.id
        )
        db.session.add(note)
        db.session.commit()
        
        self.assertFalse(note.is_completed)
        
        note.is_completed = True
        db.session.commit()
        
        self.assertTrue(note.is_completed)
    
    def test_cascade_delete(self):
        """Test: Al eliminar un usuario, se eliminan sus notas"""
        note = Note(
            title='Test Note',
            content='Content',
            user_id=self.user.id
        )
        db.session.add(note)
        db.session.commit()
        
        note_id = note.id
        
        db.session.delete(self.user)
        db.session.commit()
        
        self.assertIsNone(Note.query.get(note_id))


if __name__ == '__main__':
    unittest.main()