echo "Habilitando artifact registry en Google Cloud..."

sudo gcloud services enable artifactregistry.googleapis.com

echo "artifact registry HABILITADO."



echo "Creando repositorio para almacenar imagenes docker..."

sudo gcloud artifacts repositories create repositorio-imagenes-docker \
    --repository-format=docker \
    --location=us-central1 \
    --description="Repositorio de imágenes Docker"

echo "Repositorio para almacenar imagenes docker CREADO."