from Infraestructura import Infraestructura

class Pozo(Infraestructura.Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Pozo", eficiencia=eficiencia)
    # ? Es el "trabajo" que hace la infraestructura
    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return

        agua = int(20 * self.multiplicador() * (self.eficiencia / 100))
        colonia.recursos["Agua"] = colonia.recursos.get("Agua", 0) + agua

        print(f"Un Pozo en {colonia.nombre} ha extraído {agua} de Agua. Eficiencia: {self.eficiencia}")
