#!/bin/bash

# Lista de servicios
services=("compras_servicio/gestor_compras" "inventario_servicio/gestor_productos" "inventario_servicio/gestor_proveedores" "inventario_servicio/gestor_stock" "logistica_servicio/generador_reportes" "logistica_servicio/generador_rutas_entrega" "logistica_servicio/gestor_entregas" "seguridad_servicio/gestor_usuarios" "ventas_servicio/generador_reportes" "ventas_servicio/gestor_ventas" "ventas_servicio/procesador_predidos" "ventas_servicio/procesador_video")

# Crear un entorno virtual para cada servicio
for service in "${services[@]}"; do
    echo "Creando entorno virtual para $service..."
    python3 -m venv ../../../backend/$service/venv
    echo "Entorno virtual creado en backend/$service/venv"
done
