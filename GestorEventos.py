import Evento
from threading import Timer
import queue

class GestorEventos:
    posibles_eventos = [
        {"tipo": "enemigos"},
        {"tipo" : "tormenta"}
    ]

    def __init__(self, eventos: queue.Queue):
        self.eventos = eventos
    