#!/bin/bash

for i in {1..10}
do
  curl -X POST http://127.0.0.1:5001/api/entregas \
  -H "Content-Type: application/json" \
  -d '{
    "punto_inicio": "bodega_a",
    "destinos": ["cliente_a", "cliente_b", "cliente_c"]
  }'
  echo "Request $i sent"
done