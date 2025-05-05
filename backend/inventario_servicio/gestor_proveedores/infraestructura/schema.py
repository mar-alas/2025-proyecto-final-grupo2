from marshmallow import Schema, fields

class ProveedorInputSchema(Schema):
    nombre = fields.String(required=True, metadata={'max_length': 100})
    email = fields.Email(required=True, metadata={'max_length': 100})
    numero_contacto = fields.String(required=True, metadata={'max_length': 20})
    pais = fields.String(required=True, metadata={'max_length': 50})
    caracteristicas = fields.String(metadata={'max_length': 500})
    condiciones_comerciales_tributarias = fields.String(metadata={'max_length': 1000})

class ProveedorResponseSchema(Schema):
    id = fields.Integer()
    nombre = fields.String()
    email = fields.String()
    numero_contacto = fields.String()
    pais = fields.String()
    caracteristicas = fields.String()
    condiciones_comerciales_tributarias = fields.String()
    fecha_registro = fields.DateTime()