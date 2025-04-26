from marshmallow import Schema, fields

class ProductoUbicacionSchema(Schema):
    id_producto = fields.Integer(required=True)
    ubicacion = fields.String(required=True, validate=lambda x: x in [
        "caja", "pasillo_principal", "pasillo_secundario", "neveras"
    ])

class VisitaClienteInputSchema(Schema):
    cliente_id = fields.Integer(required=True)
    vendedor_id = fields.Integer(required=True)
    fecha = fields.String(required=True)
    ubicacion_productos_ccp = fields.List(fields.Nested(ProductoUbicacionSchema), required=True)
    ubicacion_productos_competencia = fields.List(fields.Nested(ProductoUbicacionSchema), required=True)

class RutaVisitasInputSchema(Schema):
    vendedor_id = fields.Integer(required=True)
    fecha = fields.String(required=True)
    cliente_id = fields.Integer(required=True)
    nombre_cliente = fields.String(required=True)
    barrio = fields.String(required=True)
    orden = fields.Integer(required=True)
    tiempo_estimado = fields.String(required=False)
    distancia = fields.String(required=False)