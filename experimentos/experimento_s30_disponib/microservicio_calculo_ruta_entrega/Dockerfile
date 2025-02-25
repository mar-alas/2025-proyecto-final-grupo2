#this runs with
#docker build -t microservicio_calculo_ruta_entrega_image .
#docker run --rm --name=microservicio_calculo_ruta_entrega_container --network=network_experiment -p 5000:5000 microservicio_calculo_ruta_entrega_image
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
