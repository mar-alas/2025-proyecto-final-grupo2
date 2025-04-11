from flask import Flask
from flask_cors import CORS
from aplicacion.lecturas.ping import ping_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.lecturas.productos import productos_lectura
from aplicacion.escrituras.crear_producto import crear_producto_bp


URL_PREFIX = '/api/v1/inventario/gestor_productos'
URL_HOME = "/"
URL_CREATE_PRODUCTS = URL_PREFIX+"/productos"

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
    app.register_blueprint(home_bp, url_prefix=URL_HOME)
    app.register_blueprint(productos_lectura, url_prefix=URL_PREFIX)
    app.register_blueprint(crear_producto_bp, url_prefix=URL_CREATE_PRODUCTS)
    return app
