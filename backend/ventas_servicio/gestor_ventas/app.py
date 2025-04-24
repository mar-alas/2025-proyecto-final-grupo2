from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.escrituras.visita_cliente import visita_cliente_bp
from aplicacion.lecturas.ruta_visitas import ruta_visitas_bp
from aplicacion.lecturas.home import home_bp
from flask_cors import CORS
import logging

URL_PREFIX = '/api/v1/ventas/gestor_ventas'
URL_PREFIX_PLANES = '/api/v1/ventas/gestor_ventas/gestor_planes_venta'
URL_HOME = "/"
# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(visita_cliente_bp, url_prefix=URL_PREFIX_PLANES)
app.register_blueprint(ruta_visitas_bp, url_prefix=URL_PREFIX)
CORS(app)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3008)