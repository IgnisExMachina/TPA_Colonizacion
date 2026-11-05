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

                    for tipo in self.recursos:
                        if evento.severidad > self.recursos[tipo]:
                            self.consumirRecurso(tipo= tipo, cantidad= self.recursos[tipo])#OJO
                        else:
                            self.consumirRecurso(tipo= tipo, cantidad= evento.severidad)  
                case "enemigos":
                    for i in range(evento.severidad):
                        if not self.colonos:
                            break
                        print(f"{evento.titulo}! {self.colonos.pop().nombre} muere en combate")#a interfaz
                case "visitas":
                    print(f"{evento.severidad} colono(s) se unen a la colonia!") #a interfaz
                    for i in range(evento.severidad):
                        self.agregarColono(Colono(nombre= ' '.join([random.choice(Colono.NOMBRES["NOMBRE"]), random.choice(Colono.NOMBRES["APELLIDO"])]), nombre_colonia= self.nombre, edad= random.randint(18, 80), nivel= random.randint(1, 10), genero= random.choice(["M", "F"])))
                case "averia":
                    if not self.infraestructuras:
                        print("Deberia hacer reroll")
                    else:
                        averiado = random.choice(self.infraestructuras)
                        if evento.severidad == 1 or evento.severidad == 2:
                            averiado.eficiencia = int(averiado.eficiencia * 1/2)
                        elif evento.severidad == 3 or evento.severidad == 4:
                            averiado.eficiencia = int(averiado.eficiencia * 1/4)
                        else:
                            self.infraestructuras.remove(averiado)
                case "desastre":
                    print("Impacto de meteorito. Colonia destruida.")
                    del self


if __name__ == '__main__':
    colo1 = Colonia("Agartha", colonos=[Colono("Pepe", "Agartha", 90, 3, "M"), Colono("Pepa", "Agartha", 90, 3, "F")], recursos={"Madera": 10, "Hierro": 20}, infraestructuras=[Infraestructura("Castillo"), Infraestructura("Granja")])
    colo1.procesar_eventos()