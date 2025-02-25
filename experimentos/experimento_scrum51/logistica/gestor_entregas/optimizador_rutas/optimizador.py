from .algoritmo.algoritmo_calculo_ruta import calcular_mejor_ruta

class Optimizador:
    def __init__(self, punto_inicio, destinos):
        self.punto_inicio = punto_inicio
        self.destinos = destinos

    def optimizar_ruta(self):
        return calcular_mejor_ruta(self.punto_inicio, self.destinos)
