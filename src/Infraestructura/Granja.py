from src.Infraestructura.Infraestructura import Infraestructura

class Granja(Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Granja", eficiencia=eficiencia)

    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return
        comida = 10 * (self.eficiencia / 100)
        print(f"Una Granja de {colonia.nombre} produce {comida} de alimento. Eficiencia: {self.eficiencia}")