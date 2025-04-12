from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.escrituras.visita_cliente import visita_cliente_bp
from aplicacion.lecturas.home import home_bp
from flask_cors import CORS

URL_PREFIX = '/api/v1/ventas/gestor_ventas'
URL_PREFIX = '/api/v1/ventas/gestor_planes_venta'
URL_HOME = "/"

app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(visita_cliente_bp, url_prefix=URL_PREFIX)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3008)