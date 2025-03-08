# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

# Copy the rest of the application code into the container
COPY . .

ENTRYPOINT ["python3"]
CMD ["generador_rutas.py"]