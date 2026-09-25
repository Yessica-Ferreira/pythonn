from model import ModeloTraduccion

class ControladorTraduccion:
    def __init__(self):
        self.modelo = ModeloTraduccion()

    def cargar_palabra(self, espanol, ingles):
        self.modelo.agregar_palabra(espanol, ingles)

    def traducir(self, espanol):
        resultado = self.modelo.buscar_traduccion(espanol)

        if resultado is not None:
            return resultado[0]

        return None
