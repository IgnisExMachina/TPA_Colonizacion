import pytest
from Colonia import Colonia
from Colono import Colono
from eventos.Evento import Evento
from Infraestructura.Mina import Mina
from Infraestructura.Granja import Granja


def test_inicializacion():
    colonia = Colonia(nombre="Kukusclan")
    assert colonia.nombre == "Kukusclan"
    assert colonia.colonos == []
    assert colonia.infraestructuras == []
    assert colonia.destruida is False
    assert colonia.recursos == {
        "Madera": 50, "Piedra": 50, "Agua": 50, "Hierro": 20,
        "Comida": 20, "Plutonio": 0, "Semillas": 2, "Plantas": 0
    }


def test_inicializacion_personalizada():
    colonia = Colonia(nombre="Alfa", recursos={"Madera": 80, "Hierro": 25})
    assert colonia.recursos["Madera"] == 80
    assert colonia.recursos["Hierro"] == 25
    assert colonia.recursos["Agua"] == 50  # conserva el valor base


def test_gestion_recursos():
    colonia = Colonia(nombre="Alfa")

    colonia.agregarRecurso("Madera", 10)
    assert colonia.recursos["Madera"] == 60

    colonia.consumirRecurso("Madera", 5)
    assert colonia.recursos["Madera"] == 55

    # no consume los recursos por insuficiencia
    colonia.consumirRecurso("Madera", 100)
    assert colonia.recursos["Madera"] == 55

    # el recurso no existe asi que lo ignora
    colonia.agregarRecurso("Uranio", 10)
    colonia.consumirRecurso("Uranio", 5)
    assert "Uranio" not in colonia.recursos


def test_gestion_colonos():
    colonia = Colonia(nombre="Alfa")
    assert colonia.verColonos() == "No hay colonos en este planeta."

    colono = Colono("Elena", "Alfa", 22, 1, "F")
    colonia.agregarColono(colono)

    assert len(colonia.colonos) == 1
    assert "Elena" in colonia.verColonos()


def test_crear_infraestructuras():
    colonia = Colonia(nombre="Alfa")

    # Mina cuesta 15 Madera, 10 Agua -> se construye
    colonia.crear_infraestructuras("Mina")
    assert len(colonia.infraestructuras) == 1
    assert isinstance(colonia.infraestructuras[0], Mina)
    assert colonia.recursos["Madera"] == 35
    assert colonia.recursos["Agua"] == 40

    # Castillo cuesta 50 Piedra, 30 Hierro, 20 Agua -> no alcanza Hierro (tiene 20)
    colonia.crear_infraestructuras("Castillo")
    assert len(colonia.infraestructuras) == 1


def test_eventos_y_desastre():
    colono_inicial = Colono("Alfredo", "Alfa", 25, 1, "M")
    colonia = Colonia(nombre="Alfa", colonos=[colono_inicial])

    try:
        colonia._aplicar_evento(Evento("tormenta", 2))  # Resta 2 a cada recurso con stock
        colonia._aplicar_evento(Evento("visitas", 2))   # Añade 2 colonos (total 3)
        colonia._aplicar_evento(Evento("enemigos", 1))  # Elimina 1 colono (quedan 2)

        assert colonia.recursos["Madera"] == 48
        assert colonia.recursos["Agua"] == 48
        assert len(colonia.colonos) == 2

        # Ahora probamos el bucle completo con desastre
        cola = colonia._gestor.eventos_env
        cola.put(Evento("desastre", 5))
        colonia.procesar_eventos()
    finally:
        colonia.detener_gestion()

    assert colonia.destruida is True
    assert colonia.colonos == []
    assert colonia.recursos == {}


def test_procesar_evento_averia():
    granja = Granja(eficiencia=100)
    colonia = Colonia(nombre="Alfa", infraestructuras=[granja])

    try:
        colonia._aplicar_evento(Evento("averia", 1))  # Baja eficiencia a 50 y luego aplicar_efecto a 40
    finally:
        colonia.detener_gestion()

    assert granja.eficiencia == 40
    assert colonia.recursos["Comida"] == 24  # 20 base + int(10 * 0.4)