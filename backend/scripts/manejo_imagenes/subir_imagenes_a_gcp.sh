echo "Cargando imagen [compras_servicio/gestor_compras] a GCP..."

sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/compras_servicio/gestor_compras:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/inventario_servicio/gestor_productos:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/inventario_servicio/gestor_proveedores:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/inventario_servicio/gestor_stock:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/logistica_servicio/generador_reportes:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/logistica_servicio/generador_rutas_entrega:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/logistica_servicio/gestor_entregas:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/seguridad_servicio/gestor_usuarios:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/ventas_servicio/generador_reportes:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/ventas_servicio/gestor_ventas:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/ventas_servicio/procesador_pedidos:latest
sudo docker push us-central1-docker.pkg.dev/proyecto-final-2-454403/repositorio-imagenes-docker/ventas_servicio/procesador_video:latest

echo "Proceso de cargue de imagen [compras_servicio/gestor_compras] terminado."

