from marshmallow import Schema, fields

class ProductoPedidoInputSchema(Schema):
    id = fields.Integer(required=True)
    cantidad = fields.Integer(required=True, validate=lambda x: x > 0)
    precio_unitario = fields.Float(required=True)

class PedidoInputSchema(Schema):
    cliente_id = fields.Integer(required=True)
    vendedor_id = fields.Integer(required=True)
    productos = fields.List(fields.Nested(ProductoPedidoInputSchema), required=True)

class ProductoPedidoResponseSchema(Schema):
    id = fields.Integer()
    producto_id = fields.Integer()
    cantidad = fields.Integer()
    precio_unitario = fields.Float()
    subtotal = fields.Float()

class PedidoResponseSchema(Schema):
    id = fields.Integer()
    cliente_id = fields.Integer()
    vendedor_id = fields.Integer()
    fecha_creacion = fields.DateTime()
    estado = fields.String()
    subtotal = fields.Float()
    total = fields.Float()
    productos = fields.List(fields.Nested(ProductoPedidoResponseSchema))