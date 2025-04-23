#!/bin/bash

# Verificar si vulture está instalado
if ! command -v vulture &> /dev/null
then
    echo "vulture no está instalado. Instalando vulture..."
    pip3 install vulture
    if [ $? -ne 0 ]; then
        echo "Hubo un error al instalar vulture. Asegúrate de tener pip instalado y acceso a internet."
        exit 1
    fi
fi

# Añadir la ruta de instalación de vulture al PATH temporalmente
export PATH=$PATH:/Library/Frameworks/Python.framework/Versions/3.12/bin

# Definir el directorio del proyecto, por defecto es el directorio actual
DIRECTORIO=${1:-.}

# Ejecutar vulture en el directorio especificado
echo "Ejecutando vulture en el directorio: $DIRECTORIO"

vulture dominio aplicacion infraestructura --min-confidence 50 --exclude "venv/*" --exclude "*/__init__.py"



