from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.escrituras.pedidos import pedidos_escritura
from aplicacion.lecturas.pedidos import pedidos_lectura

URL_PREFIX = '/api/v1/ventas/procesador_pedidos'
URL_HOME = "/"

app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(pedidos_escritura, url_prefix=URL_PREFIX)
app.register_blueprint(pedidos_lectura, url_prefix=URL_PREFIX)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3009)