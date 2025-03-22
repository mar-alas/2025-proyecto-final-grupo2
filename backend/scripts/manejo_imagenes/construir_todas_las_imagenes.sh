#!/bin/bash

# Configuración
PLATFORM="linux/amd64"
REPO_BASE="us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker"
DOCKERFILES_DIR="../../Dockerfiles"

# Definir manualmente los builds

echo "🚀 Construyendo imagen para compras_servicio/gestor_compras desde $DOCKERFILES_DIR/Dockerfile.gestor_compras..."

ERROR_LOG=$(
docker buildx build --platform linux/amd64 \
  -t us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/compras_servicio/gestor_compras:latest \
  -f ../../Dockerfiles/Dockerfile.gestor_compras \
  --build-context seedwork_compartido=../../../backend/seedwork_compartido \
  ../../
)


# Verificar si el build fue exitoso
if [ $? -ne 0 ]; then
  echo "❌ Error construyendo la imagen para compras_servicio/gestor_compras"
  echo "🔍 Detalles del error:"
  echo "$ERROR_LOG"
  exit 1
fi

echo "✅ Imagen para compras_servicio/gestor_compras construida exitosamente."

echo "🎉 ¡Todas las imágenes han sido construidas!"
