import random

import pytest
from Infraestructura.Huerto import Huerto


class ColoniaTest:
    def __init__(self, nombre: str, semillas: int = 0):
        self.nombre = nombre
        self.recursos = {"Semillas": semillas, "Plantas": 0}


def hacer_crecer(huerto, colonia, eventos):
    for _ in range(eventos):
        huerto.eficiencia = 100  # que el desgaste no pare el crecimiento en el test
        huerto.aplicar_efecto(colonia)


def test_plantar_gasta_una_semilla():
    colonia = ColoniaTest("Alfa", semillas=2)
    huerto = Huerto()
    assert huerto.plantar(colonia) is True
    assert colonia.recursos["Semillas"] == 1
    assert huerto.plantas == [0]


def test_no_se_planta_sin_semillas():
    colonia = ColoniaTest("Alfa", semillas=0)
    huerto = Huerto()
    assert huerto.plantar(colonia) is False
    assert huerto.plantas == []


def test_no_se_planta_con_el_huerto_lleno():
    colonia = ColoniaTest("Alfa", semillas=100)
    huerto = Huerto()
    for _ in range(huerto.num_parcelas()):
        assert huerto.plantar(colonia) is True
    assert huerto.plantar(colonia) is False
    assert len(huerto.plantas) == huerto.num_parcelas()


def test_las_plantas_maduran_con_los_eventos():
    colonia = ColoniaTest("Alfa", semillas=1)
    huerto = Huerto()
    huerto.plantar(colonia)
    hacer_crecer(huerto, colonia, Huerto.EVENTOS_PARA_CRECER - 1)
    assert huerto.plantas_maduras() == 0
    hacer_crecer(huerto, colonia, 1)
    assert huerto.plantas_maduras() == 1


def test_recoger_solo_las_maduras():
    random.seed(0)
    colonia = ColoniaTest("Alfa", semillas=3)
    huerto = Huerto()
    huerto.plantar(colonia)
    huerto.plantar(colonia)
    hacer_crecer(huerto, colonia, Huerto.EVENTOS_PARA_CRECER)
    huerto.plantar(colonia)  # esta todavia no esta madura

    cosecha = huerto.recoger(colonia)
    assert cosecha["Plantas"] == 2
    assert 0 <= cosecha["Semillas"] <= 2 * Huerto.MAX_SEMILLAS_POR_PLANTA
    assert colonia.recursos["Plantas"] == 2
    assert colonia.recursos["Semillas"] == cosecha["Semillas"]
    assert huerto.plantas == [0]


def test_recoger_sin_plantas_maduras_no_da_nada():
    colonia = ColoniaTest("Alfa")
    huerto = Huerto()
    assert huerto.recoger(colonia) == {"Plantas": 0, "Semillas": 0}


@pytest.mark.parametrize("nivel, parcelas", [(1, 6), (2, 8), (5, 14)])
def test_invertir_da_mas_parcelas(nivel, parcelas):
    huerto = Huerto()
    huerto.nivel = nivel
    assert huerto.num_parcelas() == parcelas
