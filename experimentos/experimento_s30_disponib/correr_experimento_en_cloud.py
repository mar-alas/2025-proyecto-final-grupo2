import requests
import random
import time
import logging
import pandas as pd
from datetime import datetime
from tqdm import tqdm


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("log_experimento_cloud.log", mode="w")
    ]
)

# URL del servicio
INGRESS_URL = "http://34.49.2.42"
PING_URL = INGRESS_URL+"/ping"
RUTAS_URL = INGRESS_URL+"/rutas"
CALCULAR_RUTA_URL = INGRESS_URL+"/calcular-ruta"

def verificar_ping():
    try:
        response = requests.get(PING_URL, headers={'content-type': 'application/json'})
        
        if response.status_code == 200:
            logging.info("✅ El servicio está funcionando correctamente.")
        else:
            logging.error(f"❌ Error: Código de estado {response.status_code}, Respuesta: {response.text}")

    except requests.RequestException as e:
        logging.error(f"🚨 Excepción al hacer la solicitud: {e}")


def eliminar_rutas_en_base_de_datos():
    try:
        response = requests.delete(RUTAS_URL, headers={'content-type': 'application/json'})
        
        if response.status_code == 200:
            logging.info("✅ Todas las rutas fueron eliminadas correctamente.")
        else:
            logging.error(f"❌ Error al eliminar rutas: Código {response.status_code}, Respuesta: {response.text}")

    except requests.RequestException as e:
        logging.error(f"🚨 Excepción al hacer la solicitud: {e}")


def consultar_rutas() -> list:
    try:
        response = requests.get(RUTAS_URL, headers={'content-type': 'application/json'})
        response.raise_for_status()  # Lanza una excepción si la respuesta no es 2xx

        data = response.json()
        logging.info(f"✅ Respuesta del servidor: {data.get('message', '')}")

        rutas = data.get("data", [])
        logging.info(f"📌 {len(rutas)} rutas encontradas.") 

        for ruta in rutas:
            logging.info(f"🛤️ ID: {ruta['id']}, Calculada: {ruta['ruta_calculada']}, Correcto: {ruta['calculo_correcto']}")

        return rutas
    except requests.RequestException as e:
        logging.error(f"🚨 Error en la solicitud: {e}")


def calcular_ruta(vector):
    """Invoca el servicio de cálculo de ruta con un vector de números enteros."""
    try:
        response = requests.post(CALCULAR_RUTA_URL, headers={"Content-Type": "application/json"}, json={"ruta_sin_calcular": vector})
        response.raise_for_status()  # Lanza una excepción si la respuesta no es 2xx

        data = response.json()
        logging.info(f"✅ Respuesta del servidor: {data}")
        return data
    except requests.RequestException as e:
        logging.error(f"🚨 Error en la solicitud: {e}")
        return None


def generar_y_enviar_rutas(numero_requests: int = 1):
    """Genera y envía rutas aleatorias al servicio de cálculo."""
    for _ in tqdm(range(numero_requests), desc="Enviando rutas"):
        vector_length = random.randint(5, 20)
        rnd_int_list = [random.randint(0, 100) for _ in range(vector_length)]
        calcular_ruta(rnd_int_list)


def exportar_rutas_a_excel(rutas: list, filename="rutas_calculadas_cloud.xlsx"):
    """Convierte la lista de rutas en un DataFrame y lo exporta a Excel."""
    if not rutas:
        logging.warning("⚠️ No hay rutas para exportar.")
        return

    # Convertir JSON a DataFrame
    df = pd.DataFrame(rutas)

    # Convertir fechas de string a datetime
    df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"])
    df["fecha_actualizacion"] = pd.to_datetime(df["fecha_actualizacion"])

    # Calcular el tiempo en milisegundos hasta la corrección
    df["miliseconds_2_correction"] = (df["fecha_actualizacion"] - df["fecha_creacion"]).dt.total_seconds() * 1000

    # Exportar a Excel
    df.to_excel(filename, index=False)
    logging.info(f"📂 Archivo Excel generado: {filename}")


# Ejecucion Experimento

# Paso 1: Limpiar BD
eliminar_rutas_en_base_de_datos()

# Paso 2: Llamar al API
numero_requests=5000
generar_y_enviar_rutas(numero_requests)

# Paso 3: Pausa para darle espacio al suscriptor que termine de consumir mensajes.
time.sleep(5)

# Paso 4: Consultar el resultado
resultado = consultar_rutas()

# Paso 5:
exportar_rutas_a_excel(rutas=resultado)
