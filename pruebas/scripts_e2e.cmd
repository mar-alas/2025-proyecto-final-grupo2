@echo off
REM Login to seguridad_servicio_db inside the Docker container and print available tables

echo Logging into seguridad_servicio_db inside Docker container...
docker exec backend-seguridad_servicio_db-1 psql -U postgres -d seguridad_servicio_db -c "\dt"

echo Erasing all table contents seguridad_servicio_db...
docker exec backend-seguridad_servicio_db-1 psql -U postgres -d seguridad_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"

echo Erasing all table contents inventario_servicio_db...
docker exec backend-inventario_servicio_db-1 psql -U postgres -d inventario_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' CASCADE'; END LOOP; END $$;"


echo Erasing all table contents logistica_servicio_db...
docker exec backend-logistica_servicio_db-1 psql -U postgres -d logistica_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"

echo Erasing all table contents compras_servicio_db...
docker exec backend-compras_servicio_db-1 psql -U postgres -d compras_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"

echo Erasing all table contents ventas_servicio_db...
docker exec backend-ventas_servicio_db-1 psql -U postgres -d ventas_servicio_db -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE'; END LOOP; END $$;"
echo All table contents erased.


echo Inserting sample data...
docker exec backend-seguridad_servicio_db-1 psql -U postgres -d seguridad_servicio_db -c "BEGIN; INSERT INTO users ( name, email, password, role, country, city, address) VALUES ( 'John Doe', 'testv@mail.com', 'scrypt:32768:8:1$pfXNyC2V7nGvSAls$50b0934adf95a2d80f1c71b91341db2b3693e66b91b9dfe06f9372e8e98565f311c2657f287930dd071688c45defbcff1b9b2b38b3e7f0c5864d6648f0c2c802', 'vendedor', 'Colombia', 'Bogota', 'Calle 123'); COMMIT;"
docker exec backend-inventario_servicio_db-1 psql -U postgres -d inventario_servicio_db -c "BEGIN; INSERT INTO productos (id, nombre, descripcion, tiempo_entrega, precio, condiciones_almacenamiento, fecha_vencimiento, estado, inventario_inicial, proveedor) VALUES (1, 'Producto A', 'Descripcion del producto A', '5 dias', 100.50, 'Almacenar en lugar seco', '2025-12-31', 'en_stock', 50, 'Proveedor A'); COMMIT;"
docker exec backend-inventario_servicio_db-1 psql -U postgres -d inventario_servicio_db -c "BEGIN; INSERT INTO stock (producto_id, inventario) VALUES (1, 50); COMMIT;"

echo Sample data inserted.
REM docker exec backend-seguridad_servicio_db-1 psql -U postgres -d seguridad_servicio_db -c "select * from users;"



