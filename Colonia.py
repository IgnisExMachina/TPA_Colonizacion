from Colono import Colono
from Infraestructura.Infraestructura import Infraestructura
from Recursos import Recursos

from GestorEventos import GestorEventos as Gestor
from Evento import Evento
import queue
import random 

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

        self._gestor = Gestor(queue.Queue(), min_interval=3, max_interval=8)
        self._stream = self.iniciar_gestor()

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

    def iniciar_gestor(self):
        self._gestor.iniciar()
        try:
            while True:
                yield self._gestor.eventos_env.get()   
        except KeyboardInterrupt:
            self._gestor.detener()

    def procesar_eventos(self):
        while True:
            evento = self._stream.__next__()
            match evento.tipo:
                case "tormenta":
                    #tormenta siempre quita recursos. severidad actúa como multiplicador
                    pass
                case "enemigos":
                    #enemigos matan colonos igual a la severidad
                    pass
                case "visitas":
                    #multi de cantidad de visitantes. se pueden unir a la colonia o no
                    pass
                case "averia":
                    #afectan a las infraestructuras. 1-2 eficiencia *1/2, 3-4 eficiencia ->0, 5 desaparece
                    pass
                case "desastre":
                    #Meteorito. rocks fall, everyone dies.
                    pass



if __name__ == '__main__':
    colo1 = Colonia("Agartha", colonos=[Colono("Pepe", "Agartha", 90, 3, "M"), Colono("Pepa", "Agartha", 90, 3, "F")], recursos=[Recursos("Rara", 50, "Madera"), Recursos("Comun", 70, "Hierro")], infraestructuras=[Infraestructura("Castillo"), Infraestructura("Granja")])
    colo1.procesar_eventos()