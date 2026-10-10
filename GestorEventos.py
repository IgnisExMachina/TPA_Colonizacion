from Evento import Evento
import random
from threading import Timer
import queue

class GestorEventos: #Un gestor de eventos por cada colonia -> añadir a constructor de colonia?
    posibles_tipos = ["enemigos", "tormenta"]

    def __init__(self, eventos_env: queue.Queue, min_interval: float = 5.0, max_interval: float = 15.0, size: int =5):
        self.eventos_env = eventos_env #eventos a enviar
        self._eventos = queue.Queue() #cola interna, privada
        self.min_interval = min_interval
        self.max_interval = max_interval
        self._size = size
        self._timer: Timer | None = None
        self._activo = False

    #Generar cola
    def generar_evento(self) -> Evento:
        tipo = random.choice(GestorEventos.posibles_tipos)
        severidad = random.randint(1, 5)
        return Evento(tipo, severidad)

    def rellenar(self):
        while self._eventos.qsize() < self._size:
            self._eventos.put(self.generar_evento())

    #Reloj
    def clk_tick(self):
        if not self._activo:
            return
        evento = self._eventos.get()
        self.eventos_env.put(evento)
        self._eventos.put(self.generar_evento())
        self.programar()

    def programar(self):
        intervalo = random.uniform(self.min_interval, self.max_interval)
        self._timer = Timer(intervalo, self.clk_tick)
        self._timer.daemon = True #para que funcione en background
        self._timer.start()

    #Control
    def iniciar(self):
        self._activo = True
        self.rellenar()
        self.programar()

    def detener(self):
        self._activo = False
        if self._timer:
            self._timer.cancel()


#PRUEBAS
if __name__ == '__main__':
    import time

    cola = queue.Queue()
    gestor = GestorEventos(cola, min_interval=3, max_interval=8)
    gestor.iniciar()

    try:
        while True:
            evento = cola.get()
            print(f"[{time.strftime('%H:%M:%S')}] {evento!r}")
    except KeyboardInterrupt:
        gestor.detener()