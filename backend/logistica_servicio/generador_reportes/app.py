from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.home import home_bp

URL_PREFIX = '/api/v1/logistica/generador_reportes'
URL_HOME = "/"

app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3004)