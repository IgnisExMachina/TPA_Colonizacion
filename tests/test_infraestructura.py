import pytest
from src.Infraestructura.Granja import Granja
from src.Infraestructura.Infraestructura import Infraestructura


class ColoniaTest:
    def __init__(self, nombre: str):
        self.nombre = nombre

@pytest.fixture
def recursos_suficientes():
    return {"Madera": 50, "Agua": 50, "Piedra": 50, "Hierro": 50}

@pytest.fixture
def recursos_insuficientes():
    # No es suficiente para una Granja (15 de Madera y 35 de Agua).
    return {"Madera": 10, "Piedra": 10, "Agua": 10, "Hierro": 10}

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
    assert recursos_suficientes["Madera"] == 35
    assert recursos_suficientes["Agua"] == 15
    assert recursos_suficientes["Piedra"] == 50
    assert recursos_suficientes["Hierro"] == 50

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

    recursos_para_reparar = {"Madera": 10, "Agua": 20}

    reparado = granja.reparar(recursos_para_reparar)
    assert reparado is True
    assert granja.eficiencia == 100

def test_validaciones_setters():
    granja = Granja()

    with pytest.raises(ValueError):
        granja.eficiencia = 150

    with pytest.raises(TypeError):
        granja.eficiencia = "alta"