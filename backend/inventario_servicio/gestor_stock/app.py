from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.lecturas.stock import stock_bp
from infraestructura.consumidor import ConsumidorStock
import threading
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_consumidor():
    consumidor = ConsumidorStock(
        topico_producto="ProductoRegistrado",
        topico_pedido="PedidoProcesado"
    )
    consumidor.escuchar()


URL_PREFIX = '/api/v1/inventario/gestor_stock'
URL_HOME = "/"


app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(stock_bp, url_prefix='/api/v1/inventario/gestor_stock')
CORS(app)

if __name__ == '__main__':
    consumidor_thread = threading.Thread(target=start_consumidor, daemon=True)
    consumidor_thread.start()
    app.run(debug=True, host="0.0.0.0", port=3002)