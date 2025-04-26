@echo off
REM Login to seguridad_servicio_db inside the Docker container and print available tables

echo Logging into seguridad_servicio_db inside Docker container...
docker exec backend-seguridad_servicio_db-1 psql -U postgres -d seguridad_servicio_db -c "\dt"

#erase all table contents but keep the tables
echo Erasing all table contents but keeping the tables...
docker exec backend-seguridad_servicio_db-1 psql -U postgres -d seguridad_servicio_db -c "TRUNCATE TABLE public.users RESTART IDENTITY"
echo All table contents erased.

