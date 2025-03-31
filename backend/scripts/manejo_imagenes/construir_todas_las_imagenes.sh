#!/bin/bash

REPO_ROOT=$(git rev-parse --show-toplevel)
if [ $? -ne 0 ]; then
  echo "❌ Error: This script must be run inside a Git repository."
  exit 1
fi
echo "📦 Repo root es: $REPO_ROOT"

# Configuración
PLATFORM="linux/amd64"
REPO_BASE="us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker"
DOCKERFILES_DIR="$REPO_ROOT/backend/Dockerfiles"
echo "📦 Usando Dockerfiles desde: $DOCKERFILES_DIR"

# Definir los servicios y sus respectivos Dockerfiles
declare -A IMAGES
IMAGES=(
  ["compras_servicio/gestor_compras"]="Dockerfile.gestor_compras"
  ["inventario_servicio/gestor_productos"]="Dockerfile.gestor_productos"
  ["inventario_servicio/gestor_proveedores"]="Dockerfile.gestor_proveedores"
  ["inventario_servicio/gestor_stock"]="Dockerfile.gestor_stock"
  ["logistica_servicio/generador_reportes"]="Dockerfile.generador_reportes_logistica"
  ["logistica_servicio/generador_rutas_entrega"]="Dockerfile.generador_rutas_entrega"
  ["logistica_servicio/gestor_entregas"]="Dockerfile.gestor_entregas"
  ["seguridad_servicio/gestor_usuarios"]="Dockerfile.gestor_usuarios"
  ["ventas_servicio/generador_reportes"]="Dockerfile.generador_reportes_ventas"
  ["ventas_servicio/gestor_ventas"]="Dockerfile.gestor_ventas"
  ["ventas_servicio/procesador_pedidos"]="Dockerfile.procesador_pedidos"
  ["ventas_servicio/procesador_video"]="Dockerfile.procesador_video"
)

# Construir imágenes
build_image() {
  local service=$1
  local dockerfile=$2

  echo "🚀 Construyendo imagen para $service desde $DOCKERFILES_DIR/$dockerfile..."

  ERROR_LOG=$(
    docker buildx build --platform "$PLATFORM" \
      -t "$REPO_BASE/$service:latest" \
      -f "$DOCKERFILES_DIR/$dockerfile" \
      --build-context seedwork_compartido="$REPO_ROOT/backend/seedwork_compartido" \
      "$REPO_ROOT"
  )

  if [ $? -ne 0 ]; then
    echo "❌ Error construyendo la imagen para $service"
    echo "🔍 Detalles del error:"
    echo "$ERROR_LOG"
    echo "🛠️ Comando ejecutado: docker buildx build --platform \"$PLATFORM\" -t \"$REPO_BASE/$service:latest\" -f \"$DOCKERFILES_DIR/$dockerfile\" --build-context seedwork_compartido=../../../backend/seedwork_compartido ../../"
    exit 1
  fi

  echo "✅ Imagen para $service construida exitosamente."
}

# Llamar a la función para cada imagen definida
# Comentar las lineas de imagenes que no queramos generar.
build_image "compras_servicio/gestor_compras" "Dockerfile.gestor_compras"
build_image "inventario_servicio/gestor_productos" "Dockerfile.gestor_productos"
build_image "inventario_servicio/gestor_proveedores" "Dockerfile.gestor_proveedores"
build_image "inventario_servicio/gestor_stock" "Dockerfile.gestor_stock"
build_image "logistica_servicio/generador_reportes" "Dockerfile.generador_reportes_logistica"
build_image "logistica_servicio/generador_rutas_entrega" "Dockerfile.generador_rutas_entrega"
build_image "logistica_servicio/gestor_entregas" "Dockerfile.gestor_entregas"
build_image "seguridad_servicio/gestor_usuarios" "Dockerfile.gestor_usuarios"
build_image "ventas_servicio/generador_reportes" "Dockerfile.generador_reportes_ventas"
build_image "ventas_servicio/gestor_ventas" "Dockerfile.gestor_ventas"
build_image "ventas_servicio/procesador_pedidos" "Dockerfile.procesador_pedidos"
build_image "ventas_servicio/procesador_video" "Dockerfile.procesador_video"


echo "🎉 ¡Todas las imágenes han sido construidas!"