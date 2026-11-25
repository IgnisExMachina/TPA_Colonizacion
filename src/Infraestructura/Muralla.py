from Infraestructura import Infraestructura

class Muralla(Infraestructura.Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Muralla", eficiencia=eficiencia)

    # ? Es el "trabajo" que hace la infraestructura
    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return
        defensa = int(20 * self.multiplicador() * (self.eficiencia / 100))
        colonia.recursos["Defensa"] = colonia.recursos.get("Defensa", 0) + defensa
        print(f"Una Muralla aumenta la defensa de {colonia.nombre} (+{defensa}). Eficiencia: {self.eficiencia}")