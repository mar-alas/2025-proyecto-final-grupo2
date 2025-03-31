from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.proveedores import proveedores_lectura
from aplicacion.lecturas.home import home_bp
from aplicacion.escrituras.proveedores import proveedores_escritura

URL_PREFIX = '/api/v1/inventario/gestor_proveedores'
URL_HOME = "/"

app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(proveedores_escritura, url_prefix=URL_PREFIX)
app.register_blueprint(proveedores_lectura, url_prefix=URL_PREFIX)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3003)