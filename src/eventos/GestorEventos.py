from .Evento import Evento
import random
from threading import Timer
import queue

class GestorEventos:
    MIN = 10.0
    MAX = 30.0
    posibles_tipos = ["enemigos", "tormenta", "visitas", "averia", "desastre"]

    def __init__(self, eventos_env: queue.Queue, min_interval: float = MIN, max_interval: float = MAX, size: int =5):
        self.eventos_env = eventos_env #eventos a enviar
        self._eventos = queue.Queue() # ! cola interna, privada. El primero que entra por el primero que sale
        self.min_interval = min_interval
        self.max_interval = max_interval
        self._size = size
        self._timer: Timer | None = None
        self._activo = False

    #? Generar cola
    def generar_evento(self) -> Evento:
        # ! CHOICE -> Función de Python. Coge un evento aleatorio de una lista. "un diccionario son 2 listas"
        # ! posibles_tipos = ["enemigos", "tormenta", "visitas", "averia", "desastre"]
        tipo = random.choice(GestorEventos.posibles_tipos)
        if tipo == "desastre": #si saca desastre, 9 de 10 veces genera otro evento
            unlucky = random.randint(1, 10)
            if unlucky == 10:
                severidad = 5
            else:
                return self.generar_evento()
        else:
            severidad = random.randint(1, 5)
        return Evento(tipo, severidad)
    
    # ? Rellenamos la cola para que siempre haya 5 eventos en ella. Se ejecuta en el __init__
    def rellenar(self):
        while self._eventos.qsize() < self._size:
            self._eventos.put(self.generar_evento())

    #Reloj
    def clk_tick(self):
        if not self._activo:
            return
        evento = self._eventos.get() # ? cogemos un evento
        self.eventos_env.put(evento) # ? Enviamos el evento a colonia
        self._eventos.put(self.generar_evento()) # ? Rellenamos el evento de nuevo
        self.programar() # ? Tiempo de ejecución de los eventos

    def programar(self):
        # ! El random.uniform es como el randint pero con decimales y nos saca un intervalo entre 10 y 30 (valores que le hemos dado en las constantes)
        intervalo = random.uniform(self.min_interval, self.max_interval)
        self._timer = Timer(intervalo, self.clk_tick) #! Timer() -> Es un hilo de Python, el clk_tick lo utilizamos sin () porque no se va a ejecutar ya mismo
        self._timer.daemon = True # ! .daemon es para que sea un hilo de fondo
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