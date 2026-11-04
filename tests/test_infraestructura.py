import pytest
from Infraestructura.Granja import Granja
from Infraestructura.Infraestructura import Infraestructura
from Recursos import Recursos


class ColoniaTest:
    def __init__(self, nombre: str):
        self.nombre = nombre


@pytest.fixture
def recursos_suficientes():
    return [
        Recursos(tipo="Madera", rareza="Común", cantidad=50),
        Recursos(tipo="Agua", rareza="Común", cantidad=50),
    ]


@pytest.fixture
def recursos_insuficientes():
    return [
        Recursos(tipo="Madera", rareza="Común", cantidad=5),
        Recursos(tipo="Agua", rareza="Común", cantidad=5),
    ]


def test_creacion_infraestructura_y_coste():
    granja = Granja()
    assert granja.tipo == "Granja"
    assert granja.eficiencia == 100
    assert granja.coste == {"Madera": 15, "Agua": 35}


def test_comprobar_recursos(recursos_suficientes, recursos_insuficientes):
    granja = Granja()
    assert granja.comprobar_recursos(recursos_suficientes) is True
    assert granja.comprobar_recursos(recursos_insuficientes) is False


def test_construir_descuenta_recursos(recursos_suficientes):
    granja = Granja()
    exito = granja.construir(recursos_suficientes)

    assert exito is True
    assert recursos_suficientes[0].cantidad == 35
    assert recursos_suficientes[1].cantidad == 15


def test_desgaste_eficiencia():
    colonia = ColoniaTest("Alfa")
    granja = Granja(eficiencia=100)

    granja.aplicar_efecto(colonia)
    assert granja.eficiencia == 90

    granja.aplicar_efecto(colonia)
    assert granja.eficiencia == 80


def test_reparacion_infraestructura():
    colonia = ColoniaTest("Alfa")
    granja = Granja()

    for i in range(10):
        granja.aplicar_efecto(colonia)

    assert granja.eficiencia == 0

    # Recursos necesarios para reparar (mitad de 15 Madera -> 7, mitad de 35 Agua -> 17)
    recursos_para_reparar = [
        Recursos(tipo="Madera", rareza="Común", cantidad=10),
        Recursos(tipo="Agua", rareza="Común", cantidad=20),
    ]

    reparado = granja.reparar(recursos_para_reparar)
    assert reparado is True
    assert granja.eficiencia == 100


def test_validaciones_setters():
    granja = Granja()

    with pytest.raises(ValueError):
        granja.eficiencia = 150

    with pytest.raises(TypeError):
        granja.eficiencia = "alta"