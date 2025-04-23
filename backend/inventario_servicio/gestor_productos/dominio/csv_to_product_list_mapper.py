import csv

def obtener_lista_productos_desde_csv(csv_file):
    csv_file.seek(0)
    reader = csv.DictReader(csv_file)

    data = []
    for row in reader:
        producto = {
            "nombre": row["nombre"].strip(),
            "descripcion": row["descripcion"].strip(),
            "tiempo_entrega": row["tiempo_entrega"].strip(),
            "precio": float(row["precio"]),
            "condiciones_almacenamiento": row["condiciones_almacenamiento"].strip(),
            "fecha_vencimiento": row["fecha_vencimiento"].strip(),
            "estado": row["estado"].strip(),
            "inventario_inicial": int(row["inventario_inicial"]),
            "imagenes_productos": [img.strip() for img in row["imagenes_productos"].split(",")],
            "proveedor": row["proveedor"].strip()
        }
        data.append(producto)

    return data
