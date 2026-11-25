from Infraestructura import Infraestructura

class Granja(Infraestructura.Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Granja", eficiencia=eficiencia)

    # ? Es el "trabajo" que hace la infraestructura
    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return
        comida = int(10 * self.multiplicador() * (self.eficiencia / 100))
        colonia.recursos["Comida"] = colonia.recursos.get("Comida", 0) + comida
        print(f"Una Granja de {colonia.nombre} produce {comida} de alimento. Eficiencia: {self.eficiencia}")