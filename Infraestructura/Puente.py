from Infraestructura.Infraestructura import Infraestructura

class Puente(Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Puente", eficiencia=eficiencia)

    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return
        print(f"Un Puente mejora el comercio y movilidad en {colonia.nombre}. Eficiencia: {self.eficiencia}")