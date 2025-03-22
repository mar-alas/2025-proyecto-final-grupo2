echo "Inicia despliegue de imagenes en k8s..."

## gestor compras
sudo kubectl apply -f ../../k8s/gestor_compras_deployment.yaml
sudo kubectl apply -f ../../k8s/gestor_compras_service.yaml

echo "Termina despliegue de imagenes en k8s."