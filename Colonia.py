from Colono import Colono
from Infraestructura.Infraestructura import Infraestructura
from Recursos import Recursos


class Colonia:
    def __init__(self, nombre: str, colonos: list = None, recursos: dict = None, infraestructuras: list = None):
        if colonos is None and recursos is None and infraestructuras is None:
            self.colonos = []
            self.recursos = {}
            self.infraestructuras = []
        else:
            self.colonos = colonos
            self.recursos = recursos
            self.infraestructuras = infraestructuras
            self.nombre = nombre

    def agregarColono(self, colono: Colono):
        self.colonos.append(colono)

    def verColonos(self): #! PONERLO MÁS BONITO CADA COLONO
        texto = ""
        if not self.colonos:
            return "No hay colonos en este planeta."
        for colono in self.colonos:
            texto += f"{colono}\n"
        return texto


    def agregarRecurso(self, tipo: str, cantidad: int):
        if tipo in self.recursos :
            self.recursos[tipo] += cantidad
        else:
            self.recursos[tipo] = cantidad

    def consumirRecurso(self, tipo: str, cantidad: int):
        if tipo in self.recursos and self.recursos[tipo] >= cantidad:
            self.recursos[tipo] -= cantidad
            print("Recursos restados correctamente")
            return
        print("Los recursos NO SE HAN RESTADO BIEN")

    def verRecursos(self):
        if not self.recursos:
            print("No hay recursos todavía")
            return
        for tipo, cantidad in self.recursos.items():
            print(f"- {tipo}: {cantidad}")

    def agregarInfraestructuras(self, infraestructura: Infraestructura):
        self.infraestructuras.append(infraestructura)

    def verInfraestructuras(self):
        for infraestructura in self.infraestructuras:
            print(infraestructura.tipo)
            print(infraestructura.eficiencia)


    @property #getter
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str):
        self._nombre = nombre

    
    






#PRUEBAS---------------------