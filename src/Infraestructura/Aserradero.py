from Infraestructura import Infraestructura

class Aserradero(Infraestructura.Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Aserradero", eficiencia=eficiencia)

    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return

        madera = int(20 * self.multiplicador() * (self.eficiencia / 100))
        colonia.recursos["Madera"] = colonia.recursos.get("Madera", 0) + madera

        print(f"Un Aserradero en {colonia.nombre} ha producido {madera} de Madera. Eficiencia: {self.eficiencia}")
