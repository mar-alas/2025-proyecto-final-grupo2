from flask import Flask
from flask_cors import CORS
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.home import home_bp

URL_PREFIX = '/api/v1/compras/gestor_compras'
URL_HOME = "/"

app = Flask(__name__)
CORS(app)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)