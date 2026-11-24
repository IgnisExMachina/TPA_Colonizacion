from Infraestructura import Infraestructura

class Castillo(Infraestructura.Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Castillo", eficiencia=eficiencia)

    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return
        moral = int(15 * self.multiplicador() * (self.eficiencia / 100))
        colonia.recursos["Moral"] = colonia.recursos.get("Moral", 0) + moral
        print(f"Un Castillo aumenta el bienestar de los colonos {colonia.nombre} (+{moral}). Eficiencia: {self.eficiencia}")