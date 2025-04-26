from flask import Flask
from flask_cors import CORS
from aplicacion.lecturas.ping import ping_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.lecturas.productos import productos_lectura
from aplicacion.escrituras.crear_producto import crear_producto_bp
from aplicacion.escrituras.crear_productos_via_csv import crear_producto_via_csv_bp
from aplicacion.lecturas.consultar_productos import consultar_productos_bp
from infraestructura.config import Config

URL_PREFIX = '/api/v1/inventario/gestor_productos'
URL_HOME = "/"
URL_CREATE_PRODUCTS = URL_PREFIX+"/productos"
URL_CREATE_PRODUCTS_VIA_CSV = URL_PREFIX+"/productos/importar-masivamente"

URL_PREFIX_V2 = "/api/v2/inventario/gestor_productos"
URL_GET_PRODUCTS_V2 = URL_PREFIX_V2 + "/productos"


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    CORS(app)

    app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
    app.register_blueprint(home_bp, url_prefix=URL_HOME)
    app.register_blueprint(productos_lectura, url_prefix=URL_PREFIX)
    app.register_blueprint(crear_producto_bp, url_prefix=URL_CREATE_PRODUCTS)
    app.register_blueprint(crear_producto_via_csv_bp, url_prefix=URL_CREATE_PRODUCTS_VIA_CSV)
    app.register_blueprint(consultar_productos_bp, url_prefix=URL_GET_PRODUCTS_V2)
    return app
