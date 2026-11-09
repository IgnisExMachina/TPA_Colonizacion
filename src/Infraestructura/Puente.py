from Infraestructura import Infraestructura

class Puente(Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Puente", eficiencia=eficiencia)

    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return

        extraccion = int(20 * (self.eficiencia / 100))
        colonia.recursos["Madera"] += extraccion
        colonia.recursos["Agua"] += extraccion

        print(f"Un Puente en {colonia.nombre} sirvió para extraer {extraccion} de Madera y Agua. Eficiencia: {self.eficiencia}")