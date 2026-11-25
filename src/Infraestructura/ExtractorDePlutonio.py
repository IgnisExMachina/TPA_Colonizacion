from Infraestructura import Infraestructura

class ExtractorDePlutonio(Infraestructura.Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="ExtractorDePlutonio", eficiencia=eficiencia)

    # ? Es el "trabajo" que hace la infraestructura
    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return

        # El plutonio es escaso: se extrae poco en cada evento
        plutonio = int(5 * self.multiplicador() * (self.eficiencia / 100))
        colonia.recursos["Plutonio"] = colonia.recursos.get("Plutonio", 0) + plutonio

        print(f"Un Extractor de Plutonio en {colonia.nombre} ha extraído {plutonio} de Plutonio. Eficiencia: {self.eficiencia}")
