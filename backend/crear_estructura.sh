# ventas_servicio
#     gestor_ventas
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
#     procesador_video
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
#     procesador_pedidos
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
#     generador_reportes
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
# logistica_servicio
#     generador_rutas_entrega
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
#     gestor_entregas
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
#     generador_reportes
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
# inventario_servicio
#     gestor_proveedores
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
#     gestor_productos
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
#     gestor_stock
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
# compras_servicio
#     gestor_compras
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork
# seguridad_servicio
#     gestor_usuarios
#         aplicacion
#             lecturas
#             escrituras
#         dominio
#         infraestructura
#         seedwork


#!/bin/bash

# Define the folder structure
folders=(
    "ventas_servicio/gestor_ventas"
    "ventas_servicio/procesador_video"
    "ventas_servicio/procesador_pedidos"
    "ventas_servicio/generador_reportes"
    "logistica_servicio/generador_rutas_entrega"
    "logistica_servicio/gestor_entregas"
    "logistica_servicio/generador_reportes"
    "inventario_servicio/gestor_proveedores"
    "inventario_servicio/gestor_productos"
    "inventario_servicio/gestor_stock"
    "compras_servicio/gestor_compras"
    "seguridad_servicio/gestor_usuarios"
)

# Create the folder structure
for folder in "${folders[@]}"; do
    mkdir -p "$folder/aplicacion/lecturas"
    mkdir -p "$folder/aplicacion/escrituras"
    mkdir -p "$folder/dominio"
    mkdir -p "$folder/infraestructura"
    mkdir -p "$folder/seedwork"
    mkdir -p "$folder/tests"

    # Create Dockerfile and requirements.txt
    touch "$folder/Dockerfile"
    touch "$folder/requirements.txt"

    # Create __init__.py in each subfolder
    touch "$folder/aplicacion/lecturas/__init__.py"
    touch "$folder/aplicacion/escrituras/__init__.py"
    touch "$folder/dominio/__init__.py"
    touch "$folder/infraestructura/__init__.py"
    touch "$folder/seedwork/__init__.py"
    touch "$folder/testing/__init__.py"
done

echo "Folder structure created successfully."
