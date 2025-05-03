from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.escrituras.generador_rutas import generador_rutas_bp

URL_PREFIX = '/api/v1/logistica/generador_rutas_entrega'
URL_HOME = "/"


app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(generador_rutas_bp, url_prefix=URL_PREFIX)

if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0", port=3005)