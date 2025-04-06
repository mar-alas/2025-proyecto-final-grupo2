import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        # Test the home route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    def test_ping_route(self):
        # Test the ping route
        response = self.app.get('/api/v1/ventas/procesador_pedidos/ping')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'pong', response.data)

if __name__ == '__main__':
    unittest.main()