from Infraestructura import Infraestructura

class Mina(Infraestructura):
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="Mina", eficiencia=eficiencia)

    def aplicar_efecto(self, colonia):
        if not super().aplicar_efecto(colonia):
            return
    
        extraccion = int(15 * (self.eficiencia / 100))
        colonia.recursos["Piedra"] += extraccion
        colonia.recursos["Hierro"] += extraccion
        
        print(f"Una Mina en {colonia.nombre} ha extraído {extraccion} de Piedra y Hierro. Eficiencia: {self.eficiencia}")