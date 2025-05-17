from sqlalchemy import create_engine, Date, text
from sqlalchemy.orm import sessionmaker
from .modelos import VisitaCliente as InfraVisitaCliente, Base
from .modelos import RutaVisita as InfraRutaVisita
from .modelos import PlanVentaVendedor

import os
import random
import logging
import random
from datetime import datetime, timedelta
from infraestructura.mappers import to_infraestructura_visita, to_plan_venta_entity
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_USERNAME = os.getenv('DB_USER', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5435")
DB_NAME = os.getenv('DB_NAME', default="ventas_servicio_db")

DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'

# Initialize the database engine
engine = None
if os.environ.get('UTEST') == "True":
    engine = create_engine("sqlite:///ventas_servicio.db")
else:
    engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Ensure all tables are created in the database
def initialize_database():
    logger.info("Verificando si las tablas de la base de datos existen...")
    try:
        Base.metadata.create_all(engine)
        logger.info("Tablas creadas exitosamente o ya existentes.")
    except Exception as e:
        logger.error(f"Error al crear las tablas en la base de datos: {e}")
        raise e

# Call the database initialization function
initialize_database()


class RepositorioPlanesVenta:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()

    def guardar_o_actualizar(self, plan_venta):
        try:
            entity = to_plan_venta_entity(plan_venta)

            existente = self.db_session.query(PlanVentaVendedor).filter_by(
                vendedor_id=entity.vendedor_id,
                fecha=entity.fecha
            ).first()

            if existente:
                existente.valor = entity.valor
            else:
                self.db_session.add(entity)

            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error al guardar el plan de venta: {e}")
            raise e


class RepositorioVisitas:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()

    def guardar(self, visita):
        """Guarda una nueva visita en la base de datos."""
        try:
            # Map the domain model to the infrastructure model
            infra_visita = to_infraestructura_visita(visita)
            self.db_session.add(infra_visita)
            self.db_session.commit()
            logger.info("Visita guardada exitosamente.")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error al guardar la visita: {e}")
            raise e


class RutasVisitas:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()
        self.agregar_datos_por_defecto()

    def obtener_rutas_por_vendedor_y_fecha(self, vendedor_id, fecha):
        """Retrieve routes for a specific vendor and date."""
        try:
            rutas = self.db_session.query(InfraRutaVisita).filter(
                InfraRutaVisita.vendedor_id == vendedor_id,
                InfraRutaVisita.fecha.cast(Date) == datetime.strptime(fecha, "%Y-%m-%d").date()
            ).all()
            return rutas
        except Exception as e:
            logger.error(f"Error al obtener las rutas: {e}")
            raise e

    # Add default data to the repository
    def agregar_datos_por_defecto(self):
        logger.info("Agregando datos por defecto a la base de datos...")
        session = Session()
        try:
            # Check if data already exists
            if not session.query(InfraRutaVisita).first():
                rutas_por_defecto = [
                    InfraRutaVisita(vendedor_id=1, fecha=datetime(2025, 4, 21, 9, 0), cliente_id=1, nombre_cliente="Carlos Gomez", barrio="El Poblado", orden=1, tiempo_estimado="0.5", distancia="5 km"),
                    InfraRutaVisita(vendedor_id=1, fecha=datetime(2025, 4, 21, 11, 0), cliente_id=2, nombre_cliente="Maria Lopez", barrio="La Floresta", orden=2, tiempo_estimado="1", distancia="10 km"),
                    InfraRutaVisita(vendedor_id=1, fecha=datetime(2025, 4, 21, 14, 0), cliente_id=3, nombre_cliente="Luis Martinez", barrio="Belén", orden=3, tiempo_estimado="0.25", distancia="2 km"),
                    InfraRutaVisita(vendedor_id=1, fecha=datetime(2025, 4, 21, 16, 0), cliente_id=4, nombre_cliente="Ana Torres", barrio="Laureles", orden=4, tiempo_estimado="2", distancia="3 km")
                ]
                session.add_all(rutas_por_defecto)
                session.commit()
                logger.info("Datos por defecto agregados exitosamente.")
            else:
                logger.info("Los datos por defecto ya existen en la base de datos.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error al agregar datos por defecto: {e}")
            raise e
        finally:
            session.close()


class RepositorioReporteClientes:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()

    def obtener_clientes_con_ventas(self, vendedor_id=None, zona=None, producto_id=None):

        try:
            condiciones = []
            parametros = {}

            if vendedor_id:
                condiciones.append(" AND p.vendedor_id = :vendedor_id")
                parametros["vendedor_id"] = vendedor_id

            if producto_id:
                condiciones.append(" AND pp.producto_id = :producto_id")
                parametros["producto_id"] = producto_id

            condicion_sql = ""
            if condiciones:
                condicion_sql = " WHERE 1=1 ".join(condiciones)

            query = text(f"""
                SELECT 
                    p.cliente_id, 
                    'direccion' AS direccion, 
                    pp.producto_id AS codigo, 
                    SUM(p.total) AS promedio_ventas
                FROM pedidos p 
                INNER JOIN productos_pedido pp ON pp.pedido_id = p.id
                {condicion_sql}
                GROUP BY p.cliente_id, pp.producto_id
            """)

            result = self.db_session.execute(query, parametros)
            filas = result.fetchall()

            clientes = []
            for fila in filas:
                cliente = {
                    "nombre": f"Cliente {fila.cliente_id}",
                    "direccion": fila.direccion,
                    "codigo": f"#{fila.codigo}",
                    "promedio_ventas": float(fila.promedio_ventas)
                }
                clientes.append(cliente)

            return clientes

        except Exception as e:
            logger.error(f"Error al obtener clientes con ventas: {e}")
            raise e

    def obtener_clientes_con_ventas_fallback(self):
        nombres = [
            "Luis Ramirez", "Carlos Perez", "Maria Fernanda Gomez", "Ana Sofia Rodriguez",
            "Jose Martinez", "Juan Camilo Torres", "Laura Herrera", "Santiago Rojas",
            "Valentina Morales", "Andres Garcia", "Camila Lopez", "Miguel Angel Castillo"
        ]

        direcciones = [
            "CL 147 # 7 - 7, Bogotá",
            "CR 30 # 1 - 10, Cali",
            "CL 2 # 11 - 20, Pasto",
            "AV 68 #10 - 9, Bogotá",
            "CL 100 # 9 - 4, Medellín",
            "AV 45 # 4 - 7, Cartagena",
            "CL 50 # 25 - 10, Barranquilla",
            "CR 15 # 80 - 22, Bucaramanga",
            "CL 60 # 12 - 55, Manizales",
            "AV 27 # 14 - 66, Pereira",
            "CL 22 # 9 - 88, Cúcuta",
            "CR 12 # 45 - 21, Neiva"
        ]

        num_clientes = random.choice([3, 5, 7, 9, 11])
        nombres_sample = random.sample(nombres, k=num_clientes)
        direcciones_sample = random.sample(direcciones, k=num_clientes)

        clientes = []
        for i in range(num_clientes):
            cliente = {
                "nombre": nombres_sample[i],
                "direccion": direcciones_sample[i],
                "codigo": f"#{random.randint(10000, 99999)}",
                "promedio_ventas": round(random.uniform(50.0, 150.0), 2)
            }
            clientes.append(cliente)

        return clientes


class RepositorioReporteVentasHistorico:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()

    def obtener_reporte_ventas_historico(self):
        logger.info("Obteniendo reporte de ventas historico...")
        try:
            query = text("""
                WITH meses AS (
                SELECT 1 AS mes UNION ALL
                SELECT 2 UNION ALL
                SELECT 3 UNION ALL
                SELECT 4 UNION ALL
                SELECT 5 UNION ALL
                SELECT 6 UNION ALL
                SELECT 7 UNION ALL
                SELECT 8 UNION ALL
                SELECT 9 UNION ALL
                SELECT 10 UNION ALL
                SELECT 11 UNION ALL
                SELECT 12
            )
            SELECT
                to_char(to_date(m.mes::text, 'MM'), 'Month') AS mes,
                COALESCE(SUM(p.total), 0) AS total_ventas
            FROM meses m
            LEFT JOIN pedidos p ON EXTRACT(MONTH FROM p.fecha_creacion) = m.mes
                AND EXTRACT(YEAR FROM p.fecha_creacion) = 2025
            GROUP BY m.mes
            ORDER BY m.mes
            """)

            result = self.db_session.execute(query)
            filas = result.fetchall()

            datos_mensuales = {}
            total = 0

            for fila in filas:
                logger.info(f"Fila: {fila}")
                nombre_mes = fila.mes.strip().lower()
                ventas_mes = float(fila.total_ventas)
                datos_mensuales[str(nombre_mes)] = ventas_mes
                total += ventas_mes

            total_fallback, datos_mensuales_fallback = self.generar_reporte_historico_ventas_fallback()

            # Orden de meses correcto
            meses_ordenados = [
                "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december"
            ]

            datos_mensuales_ordenados = {
                mes: datos_mensuales.get(mes, 0) for mes in meses_ordenados
            }

            datos_mensuales_fallback_ordenado = {
                mes: datos_mensuales_fallback.get(mes, 0) for mes in meses_ordenados
            }

            return total, datos_mensuales_ordenados, total_fallback, datos_mensuales_fallback_ordenado

        except Exception as e:
            logger.error(f"Error al obtener reporte de ventas historico: {e}")
            raise e
    

    def generar_reporte_historico_ventas_fallback(self):
        meses = [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"
        ]

        datos_mensuales = {}
        total = 0

        for mes in meses:
            valor = random.randint(1500, 20000)
            datos_mensuales[str(mes)] = valor
            total += valor

        return total, datos_mensuales
    

class RepositorioMetasPlanes:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()

    def generar_hora_aleatoria(self, inicio="09:00", fin="19:00"):
        formato = "%H:%M"
        hora_inicio = datetime.strptime(inicio, formato)
        hora_fin = datetime.strptime(fin, formato)
        delta = hora_fin - hora_inicio
        segundos_aleatorios = random.randint(0, int(delta.total_seconds()))
        hora_resultado = hora_inicio + timedelta(seconds=segundos_aleatorios)
        return hora_resultado.strftime(formato)

    def generar_metas_ventas(self, n=10):
        acciones = [
            "Cerrar trato con", "Llamar a", "Enviar propuesta a",
            "Agendar cita con", "Actualizar CRM con", "Hacer seguimiento a",
            "Coordinar entrega a", "Finalizar cotización para",
            "Presentar demo a", "Enviar reporte a"
        ]
        objetos = [
            "cliente potencial", "distribuidor regional", "empresa interesada",
            "cliente VIP", "prospecto del sur", "contacto nuevo",
            "cliente corporativo", "cliente del ecommerce", "empresa B2B", "cliente antiguo"
        ]
        metas = []

        for _ in range(n):
            meta = f"{random.choice(acciones)} {random.choice(objetos)}"
            tiempo = self.generar_hora_aleatoria()
            metas.append({
                "meta": meta, 
                "tiempo": tiempo
            })

        return metas

    def generar_planes_ventas(self, n=10):
        planes_base = [
            "Lanzar campaña de", "Diseñar estrategia de", "Capacitar equipo en",
            "Optimizar proceso de", "Segmentar base de", "Implementar política de",
            "Planificar acciones para", "Estudiar competencia en", "Revisar estructura de", "Proponer mejora en"
        ]
        objetivos = [
            "ventas digitales", "captación de leads", "retención de clientes",
            "upselling", "ventas cruzadas", "promociones mensuales",
            "presentaciones comerciales", "gestión de precios", "CRM", "feedback del cliente"
        ]
        planes = []

        for _ in range(n):
            plan = f"{random.choice(planes_base)} {random.choice(objetivos)}"
            tiempo = self.generar_hora_aleatoria()
            planes.append({
                "plan": plan, 
                "tiempo": tiempo
            })

        return planes