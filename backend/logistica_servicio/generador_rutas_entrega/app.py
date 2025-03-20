from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp

URL_PREFIX = '/api/v1/logistica/generador_rutas_entrega'

app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3005)