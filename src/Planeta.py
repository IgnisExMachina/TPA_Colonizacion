from Colonia import Colonia
from Colono import Colono
from Infraestructura.Infraestructura import Infraestructura
class Planeta:
    def __init__(self, nombrePlaneta: str):
        self.nombre = nombrePlaneta
        self.recursosDisponibles = {}
        self.colonia = None

    @property #getter
    def nombre(self)-> str :
        return self._nombre

    @nombre.setter
    def nombre(self, nombre:str):
        if not nombre:
            raise("El nombre del planeta no puede estar vacío")
        self._nombre = nombre.strip()

    def fundarColonia(self, colonia):
        if self.colonia is not None:
            raise ValueError("No puedes crear una nueva colonia, este planeta ya ha sido colonizado anteriormente!")
        self.colonia = colonia
        print(f"El planeta {self.nombre} ha sido colonizado por la colonia {colonia.nombre}")
        