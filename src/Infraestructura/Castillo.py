from src.Infraestructura.Infraestructura import Infraestructura

class Castillo(Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Castillo", eficiencia=eficiencia)

    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return
        moral = 15 * (self.eficiencia / 100)
        print(f"Un Castillo aumenta el bienestar de los colonos {colonia.nombre} (+{moral}). Eficiencia: {self.eficiencia}")