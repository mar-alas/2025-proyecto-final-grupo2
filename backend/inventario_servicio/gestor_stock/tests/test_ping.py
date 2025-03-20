import unittest
from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(ping_bp, url_prefix='/api/v1/inventario/gestor_stock')
        self.client = self.app.test_client()

    def test_ping(self):
        response = self.client.get('/api/v1/inventario/gestor_stock/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "pong"})

if __name__ == '__main__':
    unittest.main()