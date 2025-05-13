from infraestructura.repositorio_entregas import RepositorioDetalleEntrega, RepositorioEntrega
from infraestructura.repositorio_camion import RepositorioCamion
from infraestructura.repositorio_entrega_camion import RepositorioEntregasProgramadas, RepositorioEntregaProgramadasDetalle
import random
import requests
import json
from infraestructura.modelos import EntregasProgramadas, EntregaProgramadaDetalle
import os
GENERADOR_RUTAS_HOSTNAME = os.getenv('GENERADOR_RUTAS_HOSTNAME', default="localhost")
GENERADOR_RUTAS_PORT = os.getenv('GENERADOR_RUTAS_PORT', default="3005")

class LogisticaEntregas:
    def __init__(self):
        """
        Constructor for LogisticaEntregas.

        :param repositorio_detalle_entrega: Repository to manage DetalleEntrega entities.
        :param repositorio_camion: Repository to manage Camion entities.
        """
        self.repositorio_detalle_entrega = RepositorioDetalleEntrega()
        self.repositorio_camion = RepositorioCamion()
        self.repositorio_entregas_programadas = RepositorioEntregasProgramadas()
        self.repositorio_entrega_programadas_detalles = RepositorioEntregaProgramadasDetalle()
        self.repositorio_entrega = RepositorioEntrega()

    def asignar_camion_a_entrega(self, entrega_id):
        """
        Assigns a Camion to a DetalleEntrega based on the entrega ID.

        :param entrega_id: ID of the entrega to which a Camion will be assigned.
        """
        # Get available camiones
        camiones_disponibles = self.repositorio_camion.obtener_camiones()
        if not camiones_disponibles:
            raise Exception("No hay camiones disponibles para asignar.")

        # Select the first available camion (or implement a selection strategy)
        camion_asignado = random.choice(camiones_disponibles)

        # Create a new DetalleEntrega with the selected camion
        detalle_entrega = {
            "entrega_id": entrega_id,
            "camion_id": camion_asignado["id"]
        }

        # Add the DetalleEntrega to the repository
        detalle_id = self.repositorio_detalle_entrega.registrar_detalle_entrega(detalle_entrega)
        return detalle_id, camion_asignado["id"]

    def asignar_entregas_programadas(self, fecha_programada, camion_id, destino):
        """
        Assigns scheduled deliveries for a given date.

        :param fecha_programada: Date for which the deliveries are scheduled.
        """
        # Get all scheduled deliveries for the given date
        entregas_programadas = self.repositorio_detalle_entrega.obtener_entregas_programadas(fecha_programada)
        if not entregas_programadas:
            raise Exception("No hay entregas programadas para la fecha dada.")

        # Assign camiones to each scheduled delivery
        for entrega in entregas_programadas:
            self.asignar_camion_a_entrega(entrega["id"])

    def convert_str_to_list(self, coordinate_str):
        return [float(coord) for coord in coordinate_str.split(',')]

    def actualizar_entregas_programadas(self, entrega_id, fecha, camion_id, destino_coordenadas, destino_direccion, origen):
        """
        1. obtener las EntregasProgramadas para ese camion en esa fecha
        2. calcular la ruta agregando el destino nuevo, si no hay entregas existentes seria la ruta origen-destino
        3. agregar la EntregasProgramadas con la nueva ruta calculada
        4. agregar la EntregasProgramadasDetalle con la entregaProgramadaId y la entregaId
        """
        entregas_programadas = self.repositorio_entregas_programadas.obtener_entregas_programadas_por_fecha_camion(fecha, camion_id)
        origen_coordenadas = self.convert_str_to_list(origen)
        destino_coordenadas = self.convert_str_to_list(destino_coordenadas)
        if not entregas_programadas:
            request_data = {"punto_inicio": {"origen": origen_coordenadas}, "destinos": {destino_direccion: {"destino": destino_coordenadas}}}
        else:
            request_data = {"punto_inicio": {"origen": origen_coordenadas}, "destinos": {}}
            for entrega in entregas_programadas:
                detalles = self.repositorio_entrega.obtener_entrega_por_id(entrega_id)
                coordenadas = detalles["coordenadas_destino"]
                # destino_coordenadas = self.convert_str_to_list(coordenadas)
                request_data["destinos"][detalles["direccion_entrega"]] = {"destino": self.convert_str_to_list(coordenadas)}
        if request_data:
            # Call the route calculation service
            response = requests.post(f"http://{GENERADOR_RUTAS_HOSTNAME}:{GENERADOR_RUTAS_PORT}/api/v1/logistica/generador_rutas_entrega/generar_ruta", json=request_data)
            # Check if the response is successful
            if response.status_code != 200:
                raise Exception("Error al calcular la ruta.")
            response_data = response.json()
            ruta_json = json.dumps(response_data)
            
            if not entregas_programadas:
                # guardar la EntregasProgramadas
                entrega_programada = EntregasProgramadas(
                    fecha_programada=fecha,
                    camion_id=camion_id,
                    ruta_calculada=ruta_json
                )
                entrega_programada_id = self.repositorio_entregas_programadas.agregar_entrega_programada(entrega_programada)
                # guardar la EntregasProgramadasDetalle
                entrega_programada_detalle = EntregaProgramadaDetalle(
                    entrega_programada_id=entrega_programada_id,
                    entrega_id=entrega_id)
                entrega_programada_detalle_id = self.repositorio_entrega_programadas_detalles.agregar_detalle(entrega_programada_detalle)
                return entrega_programada_id, entrega_programada_detalle_id
            else:
                # guardar entregaProgramadaDetalle
                entrega_programada_id = entregas_programadas[0].id
                entrega_programada_detalle = EntregaProgramadaDetalle(
                    entrega_programada_id=entrega_programada_id,
                    entrega_id=entrega_id)
                entrega_programada_detalle_id = self.repositorio_entrega_programadas_detalles.agregar_detalle(entrega_programada_detalle)
                # actualizar la ruta de entregaProgramada
                datos_actualizar = {
                    "ruta_calculada": ruta_json
                }
                self.repositorio_entregas_programadas.actualizar_entrega_programada(entrega_programada_id, datos_actualizar)
                return entrega_programada_id, entrega_programada_detalle_id
