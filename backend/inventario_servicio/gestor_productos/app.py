from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.lecturas.productos import productos_lectura

URL_PREFIX = '/api/v1/inventario/gestor_productos'
URL_HOME = "/"

app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(productos_lectura, url_prefix=URL_PREFIX)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3001)