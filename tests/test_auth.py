import unittest
from app import create_app, db
from app.models import User

class TestAuthRoutes(unittest.TestCase):
    """Pruebas unitarias para las rutas de autenticación"""
    
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
    
    def tearDown(self):
        """Limpieza después de cada test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_register_page_loads(self):
        """Test: La página de registro carga correctamente"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
    
    def test_login_page_loads(self):
        """Test: La página de login carga correctamente"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_register_success(self):
        """Test: Registro exitoso de un usuario"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')
    
    def test_register_duplicate_username(self):
        """Test: No se puede registrar un username duplicado"""
        user = User(username='existinguser', email='existing@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/register', data={
            'username': 'existinguser',
            'email': 'newemail@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=True)
        
        self.assertIn(b'nombre de usuario ya', response.data)
    
    def test_register_password_mismatch(self):
        """Test: Las contraseñas deben coincidir en el registro"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_confirm': 'differentpassword'
        }, follow_redirects=True)
        
        self.assertIn(b'no coinciden', response.data)
    
    def test_register_short_password(self):
        """Test: La contraseña debe tener al menos 6 caracteres"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': '12345',
            'password_confirm': '12345'
        }, follow_redirects=True)
        
        self.assertIn(b'al menos 6 caracteres', response.data)
    
    def test_login_success(self):
        """Test: Login exitoso con credenciales correctas"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenido', response.data)
    
    def test_login_invalid_credentials(self):
        """Test: Login falla con credenciales incorrectas"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        self.assertIn(b'incorrectos', response.data)
    
    def test_logout(self):
        """Test: Logout funciona correctamente"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'cerrado', response.data)


if __name__ == '__main__':
    unittest.main()