#!/bin/bash
set -e

# Borrar cache
rm -rf .pytest_cache
find . -type d -name "__pycache__" -exec rm -r {} +

cd "$(dirname "$0")"

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements-test-gestor-productos.txt

coverage run --source=. -m pytest tests
coverage report -m