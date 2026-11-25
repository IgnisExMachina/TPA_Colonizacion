import queue
import random
import pytest
from eventos.Evento import Evento
from eventos.GestorEventos import GestorEventos


#Tests de evento

@pytest.mark.parametrize("tipo,severidad,nombre_esperado", [
    ("tormenta", 1, "Llovizna"),
    ("tormenta", 5, "Huracán"),
    ("enemigos", 3, "Ataque"),
    ("visitas", 2, "Viajeros"),
    ("averia", 4, "Fallo Estructural"),
    ("desastre", 5, "Meteorito"),
    ("alienigenas", 1, "Evento Desconocido"),
    ("desastre", 2, "Evento Desconocido"),
])

def test_crear_evento(tipo, severidad, nombre_esperado):
    evento = Evento(tipo, severidad)
    assert evento.tipo == tipo
    assert evento.severidad == severidad
    assert evento.titulo == nombre_esperado


def test_evento_repr():
    evento = Evento("tormenta", 3)
    assert repr(evento) == "Evento: Tormenta(tipo=tormenta, severidad=3)"


#Test de Gestor de Eventos

def test_generar_evento():
    gestor = GestorEventos(queue.Queue())

    for _ in range(100):
        ev = gestor.generar_evento()
        assert isinstance(ev, Evento)
        assert ev.tipo in GestorEventos.posibles_tipos
        if ev.tipo == "desastre":
            assert ev.severidad == 5
        else:
            assert 1 <= ev.severidad <= 5


def test_rellenar_cola():
    gestor = GestorEventos(queue.Queue(), size=5)
    assert gestor._eventos.qsize() == 0

    gestor.rellenar()
    assert gestor._eventos.qsize() == 5


def test_clk_tick():
    cola_salida = queue.Queue()
    gestor = GestorEventos(cola_salida, min_interval=60.0, max_interval=120.0, size=5)
    gestor.rellenar()

    try:
        #Si esta inactivo, clk_tick no debe mover eventos
        gestor._activo = False
        gestor.clk_tick()
        assert cola_salida.empty()

        #Si est activo, saca un evento de _eventos hacia eventos_env y repone _eventos a 5
        gestor._activo = True
        gestor.clk_tick()
        assert cola_salida.qsize() == 1
        assert gestor._eventos.qsize() == 5
    finally:
        #para no dejar hilos abiertos
        gestor.detener()


def test_iniciar_y_detener_gestor():
    gestor = GestorEventos(queue.Queue(), min_interval=60.0, max_interval=120.0, size=3)
    try:
        gestor.iniciar()
        assert gestor._activo is True
        assert gestor._eventos.qsize() == 3
        assert gestor._timer is not None
        assert gestor._timer.is_alive() is True
    finally:
        gestor.detener()

    assert gestor._activo is False