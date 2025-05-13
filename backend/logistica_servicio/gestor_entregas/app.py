from flask import Flask
from flask_cors import CORS
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.lecturas.entregas import consulta_entregas_bp
from aplicacion.lecturas.entrega_detallada import entrega_detallada_bp
from aplicacion.lecturas.ubicacion_pedido import ubicacion_pedido_bp
from aplicacion.lecturas.obtener_ruta import consulta_camiones_bp
from aplicacion.escrituras.asignar_ruta import asignar_ruta_bp
from infraestructura.consumidor import ConsumidorLogistica
import threading

URL_PREFIX = '/api/v1/logistica/gestor_entregas'
URL_HOME = "/"

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(consulta_entregas_bp, url_prefix=URL_PREFIX)
app.register_blueprint(entrega_detallada_bp, url_prefix=URL_PREFIX)
app.register_blueprint(ubicacion_pedido_bp, url_prefix=URL_PREFIX)
app.register_blueprint(consulta_camiones_bp, url_prefix=URL_PREFIX)
app.register_blueprint(asignar_ruta_bp, url_prefix=URL_PREFIX)

if __name__ == '__main__':
    consumidor_logistica = ConsumidorLogistica(topico_pedido="PedidoCreado")
    listener_thread = threading.Thread(target=consumidor_logistica.escuchar, kwargs={"max_iterations": None})
    listener_thread.start()
    app.run(debug=True, host="0.0.0.0", port=3006)