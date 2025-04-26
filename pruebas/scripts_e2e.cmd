@echo off
REM Login to seguridad_servicio_db inside the Docker container and print available tables

echo Logging into seguridad_servicio_db inside Docker container...
docker exec backend-seguridad_servicio_db-1 psql -U postgres -d seguridad_servicio_db -c "\dt"

#erase all table contents but keep the tables
echo Erasing all table contents but keeping the tables...
docker exec backend-seguridad_servicio_db-1 psql -U postgres -d seguridad_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"
docker exec backend-inventario_servicio_db-1 psql -U postgres -d inventario_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"
docker exec backend-logistica_servicio_db-1 psql -U postgres -d logistica_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"
docker exec backend-compras_servicio_db-1 psql -U postgres -d compras_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"
docker exec backend-ventas_servicio_db-1 psql -U postgres -d ventas_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"
echo All table contents erased.


#insert data into productos table
echo Inserting sample data...

docker exec backend-inventario_servicio_db-1 psql -U postgres -d inventario_servicio_db -c "INSERT INTO productos (id, nombre, descripcion, tiempo_entrega, precio, condiciones_almacenamiento, fecha_vencimiento, estado, inventario_inicial, proveedor) VALUES (1, 'Producto A', 'Descripcion del producto A', '5 dias', 100.50, 'Almacenar en lugar seco', '2025-12-31', 'en_stock', 50, 'Proveedor A');"

docker exec backend-inventario_servicio_db-1 psql -U postgres -d inventario_servicio_db -c "INSERT INTO stock (producto_id, inventario) VALUES (1, 50);"


