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
    assert colonia.recursos == {"Madera": 15, "Piedra": 10, "Agua": 35, "Hierro": 10, "Comida": 10, "Moral": 30, "Defensa": 0}


def test_inicializacion_personalizada():
    colonia = Colonia(nombre="Alfa", recursos={"Madera": 50, "Hierro": 25})
    assert colonia.recursos["Madera"] == 50
    assert colonia.recursos["Hierro"] == 25
    assert colonia.recursos["Agua"] == 35  #deberia tener el valor base


def test_gestion_recursos():
    colonia = Colonia(nombre="Alfa")

    colonia.agregarRecurso("Madera", 10)
    assert colonia.recursos["Madera"] == 25

    colonia.consumirRecurso("Madera", 5)
    assert colonia.recursos["Madera"] == 20

    #no consume los recursos por insuficiencia
    colonia.consumirRecurso("Madera", 100)
    assert colonia.recursos["Madera"] == 20

    #el recurso no existe asi que lo ignora
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

    #una mina cuesta 10 Madera, 10 Hierro, 10 Agua -> se debe de construir
    colonia.crear_infraestructuras("Mina")
    assert len(colonia.infraestructuras) == 1
    assert isinstance(colonia.infraestructuras[0], Mina)
    assert colonia.recursos["Madera"] == 5

    #un castillo cuesta 50 Piedra, 30 Hierro, 20 Agua -> no alcanza con los recuros por default
    colonia.crear_infraestructuras("Castillo")
    assert len(colonia.infraestructuras) == 1


def test_eventos():
    colono_inicial = Colono("Alfredo", "Alfa", 25, 1, "M")
    colonia = Colonia(nombre="Alfa", colonos=[colono_inicial])

    cola = colonia._gestor.eventos_env
    cola.put(Evento("tormenta", 2))   # Resta 2 a cada recurso
    cola.put(Evento("visitas", 2))    # Añade 2 colonos (total 3)
    cola.put(Evento("enemigos", 1))   # Elimina 1 colono (quedan 2)
    cola.put(Evento("desastre", 5))   # Destruye la colonia y detiene el bucle

    try:
        colonia.procesar_eventos()
    finally:
        colonia.detener_gestion()

    assert colonia.recursos["Madera"] == 13
    assert colonia.recursos["Agua"] == 33
    assert len(colonia.colonos) == 2
    assert colonia.destruida is True


def test_procesar_evento_averia():
    granja = Granja(eficiencia=100)
    colonia = Colonia(nombre="Alfa", infraestructuras=[granja])

    cola = colonia._gestor.eventos_env
    cola.put(Evento("averia", 1))     # Baja eficiencia a la mitad (50) y aplica efecto (-10 -> 40)
    cola.put(Evento("desastre", 5))   # Detiene el bucle

    try:
        colonia.procesar_eventos()
    finally:
        colonia.detener_gestion()

    assert granja.eficiencia == 40
    assert colonia.recursos["Comida"] == 14.0  # 10 base + 4 producidos al 40%