### Lista de vendedores
curl --request GET \
  --url http://localhost:3011/api/v1/seguridad/gestor_usuarios/r/vendedores \
  --header 'authorization: Bearer token'

### Lista de productos:
curl --request GET \
  --url http://localhost:3011/api/v1/inventario/gestor_productos/productos

### Lista de zonas:
curl --request GET \
  --url http://localhost:3011/api/v1/inventario/gestor_productos/zonas


### Tabla de clientes con ventas
curl --request GET \
  --url http://localhost:3008/api/v1/ventas/gestor_ventas/reporte/clientes-ventas \
  --header 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsInJvbGUiOiJkaXJlY3Rvci1jb21wcmFzIiwiZXhwIjoxNzQ3NjgxNDM0fQ.GWx5BLta4__r16upddO4wBSQNPDXzO1Ld46BP78hYgs'

#### Ejemplo de response
{
  "clientes": [
    {
      "codigo": "#88013",
      "direccion": "CL 100 # 9 - 4, Medellín",
      "nombre": "Santiago Rojas",
      "promedio_ventas": 89.14
    },
    {
      "codigo": "#13524",
      "direccion": "CR 12 # 45 - 21, Neiva",
      "nombre": "Andres Garcia",
      "promedio_ventas": 141.27
    },
    {
      "codigo": "#70520",
      "direccion": "AV 68 #10 - 9, Bogotá",
      "nombre": "Laura Herrera",
      "promedio_ventas": 76.48
    },
    {
      "codigo": "#22967",
      "direccion": "AV 45 # 4 - 7, Cartagena",
      "nombre": "Jose Martinez",
      "promedio_ventas": 106.64
    },
    {
      "codigo": "#60594",
      "direccion": "CR 30 # 1 - 10, Cali",
      "nombre": "Ana Sofia Rodriguez",
      "promedio_ventas": 132.3
    },
    {
      "codigo": "#54148",
      "direccion": "AV 27 # 14 - 66, Pereira",
      "nombre": "Valentina Morales",
      "promedio_ventas": 114.12
    },
    {
      "codigo": "#55121",
      "direccion": "CL 147 # 7 - 7, Bogotá",
      "nombre": "Carlos Perez",
      "promedio_ventas": 126.65
    }
  ],
  "fallback": true
}

### Historico de ventas
curl --request GET \
  --url http://localhost:3008/api/v1/ventas/gestor_ventas/reporte/historico-ventas \
  --header 'authorization: Bearer token'

#### Ejemplo de response
{
  "historico_ventas": {
    "datos_mensuales": {
      "april": 0,
      "august": 0,
      "december": 0,
      "february": 0,
      "january": 0,
      "july": 0,
      "june": 0,
      "march": 0,
      "may": 0,
      "november": 0,
      "october": 0,
      "september": 0
    },
    "total": 0
  },
  "historico_ventas_fallback": {
    "datos_mensuales": {
      "april": 12164,
      "august": 17603,
      "december": 3902,
      "february": 13852,
      "january": 13385,
      "july": 7137,
      "june": 3546,
      "march": 2304,
      "may": 19171,
      "november": 8515,
      "october": 10718,
      "september": 18459
    },
    "total": 130756
  }
}


### Ver planes y metas
curl --request GET \
  --url http://localhost:3008/api/v1/ventas/gestor_ventas/reporte/planes-y-metas \
  --header 'authorization: Bearer token'

#### Ejemplo de response
{
  "metas": [
    {
      "meta": "Coordinar entrega a cliente del ecommerce",
      "tiempo": "09:47"
    },
    {
      "meta": "Llamar a distribuidor regional",
      "tiempo": "18:35"
    },
    {
      "meta": "Enviar propuesta a prospecto del sur",
      "tiempo": "15:46"
    },
    {
      "meta": "Enviar reporte a cliente potencial",
      "tiempo": "09:27"
    },
    {
      "meta": "Coordinar entrega a contacto nuevo",
      "tiempo": "13:06"
    },
    {
      "meta": "Enviar reporte a cliente antiguo",
      "tiempo": "17:11"
    },
    {
      "meta": "Actualizar CRM con distribuidor regional",
      "tiempo": "17:47"
    },
    {
      "meta": "Cerrar trato con prospecto del sur",
      "tiempo": "12:59"
    },
    {
      "meta": "Enviar reporte a cliente VIP",
      "tiempo": "14:46"
    },
    {
      "meta": "Agendar cita con empresa interesada",
      "tiempo": "14:16"
    }
  ],
  "planes": [
    {
      "plan": "Estudiar competencia en upselling",
      "tiempo": "09:18"
    },
    {
      "plan": "Capacitar equipo en ventas cruzadas",
      "tiempo": "09:11"
    },
    {
      "plan": "Estudiar competencia en presentaciones comerciales",
      "tiempo": "13:48"
    },
    {
      "plan": "Diseñar estrategia de upselling",
      "tiempo": "15:14"
    },
    {
      "plan": "Implementar política de ventas digitales",
      "tiempo": "15:55"
    },
    {
      "plan": "Estudiar competencia en ventas digitales",
      "tiempo": "10:11"
    },
    {
      "plan": "Optimizar proceso de upselling",
      "tiempo": "11:26"
    },
    {
      "plan": "Planificar acciones para CRM",
      "tiempo": "09:48"
    },
    {
      "plan": "Implementar política de retención de clientes",
      "tiempo": "11:52"
    },
    {
      "plan": "Estudiar competencia en retención de clientes",
      "tiempo": "15:25"
    }
  ]
}