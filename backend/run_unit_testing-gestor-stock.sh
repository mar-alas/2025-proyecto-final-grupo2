#!/bin/bash
set -e

# Borrar cache
rm -rf .pytest_cache
find . -type d -name "__pycache__" -exec rm -r {} +

cd "$(dirname "$0")"

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements-test-gestor-stock

export PYTHONPATH=$PWD                                                                                  
export UTEST=True 

coverage run --omit="/tests/,*/_init_.py" -m unittest discover -s inventario_servicio/gestor_stock
coverage report --fail-under=80