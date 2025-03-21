#!/bin/bash

# Lista de servicios (sin seedwork_compartido)
services=("compras_servicio/gestor_compras" "inventario_servicio/gestor_productos" "inventario_servicio/gestor_proveedores" "inventario_servicio/gestor_stock" "logistica_servicio/generador_reportes" "logistica_servicio/generador_rutas_entrega" "logistica_servicio/gestor_entregas" "seguridad_servicio/gestor_usuarios" "ventas_servicio/generador_reportes" "ventas_servicio/gestor_ventas" "ventas_servicio/procesador_predidos" "ventas_servicio/procesador_video")

# Instalar dependencias en cada entorno virtual
for service in "${services[@]}"; do
    if [ -d "../../../backend/$service/venv" ]; then
        echo "Activando entorno virtual para $service..."
        source ../../../backend/$service/venv/bin/activate

        # Instalar las dependencias desde requirements.txt si existe
        if [ -f "../../../backend/$service/requirements.txt" ]; then
            echo "Instalando dependencias para $service..."
            pip install -r ../../../backend/$service/requirements.txt
            echo "Dependencias instaladas para $service"
        else
            echo "No se encontró el archivo requirements.txt en $service"
        fi

        deactivate
    else
        echo "El entorno virtual para $service no existe. Por favor ejecuta crear_venv.sh primero."
    fi
done
