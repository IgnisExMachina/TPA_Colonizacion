import pytest
from Colonia import Colonia
from Colono import Colono
from GestorPersistencia import GestorPersistencia
from Infraestructura.NaveEspacial import NaveEspacial


def crear_tripulacion(cantidad: int = 5) -> list[Colono]:
    return [Colono(f"Tripulante {i}", "Alfa", 25 + i, 1, "M") for i in range(cantidad)]


def test_creacion_nave_espacial():
    nave = NaveEspacial()
    assert nave.tipo == "NaveEspacial"
    assert nave.eficiencia == 100
    assert nave.tripulacion == []
    assert nave.requisitos == {"Plantas": 0, "Plutonio": 0}
    assert nave.modificador == 1.0


def test_construir_nave_en_colonia():
    colonia = Colonia("Alfa", recursos={"Hierro": 40, "Piedra": 60, "Agua": 120})
    colonia.crear_infraestructuras("NaveEspacial")

    assert len(colonia.infraestructuras) == 1
    assert isinstance(colonia.infraestructuras[0], NaveEspacial)
    assert colonia.recursos["Hierro"] == 10
    assert colonia.recursos["Piedra"] == 10
    assert colonia.recursos["Agua"] == 20


def comprobacion_tripulacion():
    colonia = Colonia("Alfa")
    nave = NaveEspacial()
    nave.requisitos = {"Plantas": 20, "Plutonio": 30}

    for colono in crear_tripulacion(4):
        nave.agregar_a_tripulacion(colono)

    assert len(nave.tripulacion) == 4
    assert nave.listo_para_despegue(colonia) is False


def test_despega_con_tripulacion_y_plantas_o_plutonio():
    colonia = Colonia("Alfa")
    nave = NaveEspacial()
    for colono in crear_tripulacion(5):
        nave.agregar_a_tripulacion(colono)

    # Con 5 tripulantes pero sin recursos no despega
    assert nave.listo_para_despegue(colonia) is False

    # Alcanza con cumplir el requisito de Plantas o Plutonio
    nave.requisitos["Plantas"] = 20
    assert nave.listo_para_despegue(colonia) is True
    nave.requisitos = {"Plantas": 0, "Plutonio": 30}
    assert nave.listo_para_despegue(colonia) is True


def test_agregar_requisitos():
    nave = NaveEspacial()
    recursos = {"Plantas": 25, "Plutonio": 10}

    nave.agregar_requisitos(recursos)

    assert nave.requisitos["Plantas"] == 20
    assert recursos["Plantas"] == 5
    assert nave.requisitos["Plutonio"] == 10
    assert recursos["Plutonio"] == 0


def test_efecto():
    colonia = Colonia("Alfa")
    nave = NaveEspacial(eficiencia=100)

    nave.aplicar_efecto(colonia)
    assert nave.eficiencia == 90


def test_persistencia_nave(tmp_path):
    gestor = GestorPersistencia(tmp_path / "nave.json")
    nave = NaveEspacial(eficiencia=80)
    nave.agregar_a_tripulacion(Colono("Elena", "Alfa", 28, 3, "F"))

    gestor.guardar_colonias([nave])
    cargada = gestor.cargar_colonias()[0]

    assert isinstance(cargada, NaveEspacial)
    assert cargada.eficiencia == 80
    assert len(cargada.tripulacion) == 1
    assert cargada.tripulacion[0].nombre == "Elena"