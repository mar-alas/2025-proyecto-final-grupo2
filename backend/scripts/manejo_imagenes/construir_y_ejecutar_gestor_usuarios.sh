#!/bin/bash

# Configuración
PLATFORM="linux/amd64"
REPO_BASE="us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker"
DOCKERFILES_DIR="../../Dockerfiles"

# Nombre del servicio y Dockerfile específico para gestor de usuarios
SERVICE="seguridad_servicio/gestor_usuarios"
DOCKERFILE="Dockerfile.gestor_usuarios"

# Función para construir la imagen
build_image() {
  echo "🚀 Construyendo imagen para $SERVICE desde $DOCKERFILES_DIR/$DOCKERFILE..."

  ERROR_LOG=$(
    docker buildx build --platform "$PLATFORM" \
      -t "$REPO_BASE/$SERVICE:latest" \
      -f "$DOCKERFILES_DIR/$DOCKERFILE" \
      --build-context seedwork_compartido=../../../backend/seedwork_compartido \
      ../../
  )

  if [ $? -ne 0 ]; then
    echo "❌ Error construyendo la imagen para $SERVICE"
    echo "🔍 Detalles del error:"
    echo "$ERROR_LOG"
    exit 1
  fi

  echo "✅ Imagen para $SERVICE construida exitosamente."
}

# Función para ejecutar la imagen
run_image() {
  echo "🚀 Ejecutando imagen para $SERVICE..."

  docker run --platform "$PLATFORM" -d -p 3011:3011 "$REPO_BASE/$SERVICE:latest"

  if [ $? -ne 0 ]; then
    echo "❌ Error ejecutando la imagen para $SERVICE"
    exit 1
  fi

  echo "✅ Imagen para $SERVICE ejecutada en http://localhost:3011"
}

# Llamar a la función para construir y luego ejecutar la imagen
build_image
run_image
