from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.escrituras.visita_cliente import visita_cliente_bp
from aplicacion.lecturas.ruta_visitas import ruta_visitas_bp
from aplicacion.lecturas.rutas_visitas_optimizada import ruta_visita_optimizada_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.escrituras.crear_plan_de_venta import crear_plan_venta_bp
from aplicacion.lecturas.consultar_clientes_con_ventas import reporte_clientes_ventas_bp
from aplicacion.lecturas.consultar_historico_ventas import reporte_historico_ventas_bp
from aplicacion.lecturas.consultar_planes_y_ventas import reporte_metas_planes_bp
from flask_cors import CORS
import logging

URL_PREFIX = '/api/v1/ventas/gestor_ventas'
URL_PREFIX_PLANES = '/api/v1/ventas/gestor_ventas/gestor_planes_venta'
URL_HOME = "/"
URL_CREAR_PLANES_DE_VENTA = URL_PREFIX+"/vendedores/planes-venta"
URL_REPORTE_CLIENTES_VENTAS = URL_PREFIX+"/reporte/clientes-ventas"
URL_REPORTE_HISTORICO_VENTAS = URL_PREFIX+"/reporte/historico-ventas"
URL_REPORTE_PLANES_Y_METAS = URL_PREFIX+"/reporte/planes-y-metas"

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(visita_cliente_bp, url_prefix=URL_PREFIX_PLANES)
app.register_blueprint(ruta_visitas_bp, url_prefix=URL_PREFIX)
app.register_blueprint(ruta_visita_optimizada_bp, url_prefix=URL_PREFIX)
app.register_blueprint(crear_plan_venta_bp, url_prefix=URL_CREAR_PLANES_DE_VENTA)
app.register_blueprint(reporte_clientes_ventas_bp, url_prefix=URL_REPORTE_CLIENTES_VENTAS)
app.register_blueprint(reporte_historico_ventas_bp, url_prefix=URL_REPORTE_HISTORICO_VENTAS)
app.register_blueprint(reporte_metas_planes_bp, url_prefix=URL_REPORTE_PLANES_Y_METAS)

CORS(app)


if __name__ == '__main__':    app.run(debug=True, host="0.0.0.0", port=3008)