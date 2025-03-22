echo "Inicia despliegue de imagenes en k8s..."


# Despliegue de Bases de datos.
sudo kubectl apply -f ../../k8s/compras_servicio_db_deployment.yaml
sudo kubectl apply -f ../../k8s/compras_servicio_db_service.yaml
sudo kubectl apply -f ../../k8s/logistica_servicio_db_deployment.yaml
sudo kubectl apply -f ../../k8s/logistica_servicio_db_service.yaml
sudo kubectl apply -f ../../k8s/seguridad_servicio_db_deployment.yaml
sudo kubectl apply -f ../../k8s/seguridad_servicio_db_service.yaml
sudo kubectl apply -f ../../k8s/ventas_servicio_db_deployment.yaml
sudo kubectl apply -f ../../k8s/ventas_servicio_db_service.yaml
sudo kubectl apply -f ../../k8s/inventario_servicio_db_deployment.yaml
sudo kubectl apply -f ../../k8s/inventario_servicio_db_service.yaml


# Broker de mensajeria:
sudo kubectl apply -f ../../k8s/pulsar_deployment.yaml
sudo kubectl apply -f ../../k8s/pulsar_service.yaml


# Servicios:
sudo kubectl apply -f ../../k8s/gestor_compras_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_compras_service.yaml

sudo kubectl apply -f ../../k8s/gestor_productos_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_productos_service.yaml

sudo kubectl apply -f ../../k8s/gestor_proveedores_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_proveedores_service.yaml

sudo kubectl apply -f ../../k8s/gestor_stock_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_stock_service.yaml

sudo kubectl apply -f ../../k8s/generador_reportes_logistica_deployment.yaml
sudo kubectl apply -f ../../k8s/generador_reportes_logistica_service.yaml

sudo kubectl apply -f ../../k8s/generador_reportes_ventas_deployment.yaml
sudo kubectl apply -f ../../k8s/generador_reportes_ventas_service.yaml

sudo kubectl apply -f ../../k8s/gestor_rutas_entrega_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_rutas_entrega_service.yaml

sudo kubectl apply -f ../../k8s/gestor_entregas_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_entregas_service.yaml

sudo kubectl apply -f ../../k8s/gestor_usuarios_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_usuarios_service.yaml

sudo kubectl apply -f ../../k8s/gestor_ventas_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_ventas_service.yaml

sudo kubectl apply -f ../../k8s/procesador_pedidos_deployment.yaml
sudo kubectl apply -f ../../k8s/procesador_pedidos_service.yaml

sudo kubectl apply -f ../../k8s/procesador_video_deployment.yaml
sudo kubectl apply -f ../../k8s/procesador_video_service.yaml


# Ingress
sudo kubectl apply -f ../../k8s/ingress.yaml


echo "Termina despliegue de imagenes en GKE."