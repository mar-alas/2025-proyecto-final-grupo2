import requests
import random
from sqlalchemy import create_engine
import time

numero_requests=1000

#delete data base
engine = create_engine('postgresql://admin:admin@localhost:5432/rutas-db')
connection = engine.connect()
result = connection.execute("DELETE FROM rutas_calculadas")
connection.close()

for i in range(numero_requests):
    vector_length=random.randint(5, 20)
    rnd_int_list = [random.randint(0, 100) for _ in range(vector_length)]
    url = "http://localhost:5000/calcular-ruta"
    headers = {"Content-Type": "application/json"}        
    data = {"ruta_sin_calcular": rnd_int_list}
    response = requests.post(url, headers=headers, json=data)
    

#wait unit experiment finishes
time.sleep(5)

#query data base
engine = create_engine('postgresql://admin:admin@localhost:5432/rutas-db')
connection = engine.connect()
result = connection.execute("SELECT * FROM rutas_calculadas")
connection.close()

#export result to excel
import pandas as pd
df = pd.DataFrame(result.fetchall())
df.columns = result.keys()
df["miliseconds_2_correction"]=(df["fecha_actualizacion"]-df["fecha_creacion"]).dt.total_seconds()*1000

df.to_excel("rutas_calculadas.xlsx", index=False)