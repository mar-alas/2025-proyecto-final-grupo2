#!/bin/bash
set -e

# Opcional: Mostrar información de los contenedores actuales
echo "Deteniendo servicios existentes (gestor_productos, inventario_servicio_db)..."

# Detiene los servicios indicados si están en ejecución.
docker-compose stop gestor_productos inventario_servicio_db 

# Elimina de forma forzada los contenedores detenidos (opcional)
docker-compose rm -f gestor_productos inventario_servicio_db

echo "Iniciando servicios..."
docker-compose up --build gestor_productos inventario_servicio_db
