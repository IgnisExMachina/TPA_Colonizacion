from Infraestructura.Infraestructura import Infraestructura

class Muralla(Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Muralla", eficiencia=eficiencia)

    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return
        defensa = 20 * (self.eficiencia / 100)
        print(f"Una Muralla aumenta la defensa de {colonia.nombre} (+{defensa}). Eficiencia: {self.eficiencia}")