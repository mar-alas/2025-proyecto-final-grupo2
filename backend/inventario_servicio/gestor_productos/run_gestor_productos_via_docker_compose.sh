#!/bin/bash

# Script to start Gestor Productos with its required services
# Usage: ./run_gestor_productos_via_docker_compose.sh

docker-compose up --build gestor_productos inventario_servicio_db pulsar