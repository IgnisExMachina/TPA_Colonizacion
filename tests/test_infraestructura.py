import pytest
from Infraestructura.Castillo import Castillo
from Infraestructura.Granja import Granja
from Infraestructura.Mina import Mina
from Infraestructura.Muralla import Muralla
from Infraestructura.Puente import Puente
from Infraestructura.Infraestructura import Infraestructura


class ColoniaTest:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.recursos = {"Comida": 0, "Madera": 0, "Piedra": 0, "Agua": 0, "Hierro": 0, "Moral": 0, "Defensa": 0}

@pytest.fixture
def colonia_prueba():
    return ColoniaTest("Alfa")

@pytest.fixture
def recursos_suficientes():
    return {"Madera": 50, "Agua": 50, "Piedra": 50, "Hierro": 50}

@pytest.fixture
def recursos_insuficientes():
    # No es suficiente para crear ninguna infraestructura
    return {"Madera": 5, "Piedra": 5, "Agua": 5, "Hierro": 5}

@pytest.mark.parametrize("clase_infra,tipo_esperado,coste_esperado", [
    (Puente, "Puente", {"Madera": 10, "Piedra": 10}),
    (Castillo, "Castillo", {"Piedra": 50, "Hierro": 30, "Agua": 20}),
    (Muralla, "Muralla", {"Piedra": 30}),
    (Granja, "Granja", {"Madera": 15, "Agua": 35}),
    (Mina, "Mina", {"Madera": 10, "Hierro": 10, "Agua": 10}),
])

def test_creacion_y_costes_infraestructuras(clase_infra, tipo_esperado, coste_esperado):
    edificio = clase_infra()
    assert edificio.tipo == tipo_esperado
    assert edificio.eficiencia == 100
    assert edificio.coste == coste_esperado

def test_comprobar_recursos(recursos_suficientes, recursos_insuficientes):
    granja = Granja()
    assert granja.comprobar_recursos(recursos_suficientes) is True
    assert granja.comprobar_recursos(recursos_insuficientes) is False

    with pytest.raises(TypeError):
        granja.comprobar_recursos(["Madera", "Agua"])

def test_construir_descuenta_recursos(recursos_suficientes, recursos_insuficientes):
    mina = Mina()
    assert mina.construir(recursos_insuficientes) is False
    assert recursos_insuficientes["Madera"] == 5

    assert mina.construir(recursos_suficientes) is True
    assert recursos_suficientes["Madera"] == 40
    assert recursos_suficientes["Hierro"] == 40
    assert recursos_suficientes["Agua"] == 40
    assert recursos_suficientes["Piedra"] == 50

def test_efectos_y_desgaste_todas_las_infraestructuras(colonia_prueba):
    granja = Granja(eficiencia=100)
    granja.aplicar_efecto(colonia_prueba)
    assert granja.eficiencia == 90
    assert colonia_prueba.recursos["Comida"] == 9.0 #se calcula con la eficiencia ya reducida

    mina = Mina(eficiencia=100)
    mina.aplicar_efecto(colonia_prueba)
    assert mina.eficiencia == 90
    assert colonia_prueba.recursos["Piedra"] == 13
    assert colonia_prueba.recursos["Hierro"] == 13

    puente = Puente(eficiencia=100)
    puente.aplicar_efecto(colonia_prueba)
    assert puente.eficiencia == 90
    assert colonia_prueba.recursos["Madera"] == 18
    assert colonia_prueba.recursos["Agua"] == 18

    castillo = Castillo(eficiencia=100)
    castillo.aplicar_efecto(colonia_prueba)
    assert castillo.eficiencia == 90
    assert colonia_prueba.recursos["Moral"] == 13.5

    muralla = Muralla(eficiencia=100)
    muralla.aplicar_efecto(colonia_prueba)
    assert muralla.eficiencia == 90
    assert colonia_prueba.recursos["Defensa"] == 18.0

def test_infraestructura_inoperativa_con_eficiencia_cero(colonia_prueba):
    mina = Mina(eficiencia=0)
    mina.aplicar_efecto(colonia_prueba)

    assert mina.eficiencia == 0
    assert colonia_prueba.recursos["Piedra"] == 0
    assert colonia_prueba.recursos["Hierro"] == 0

def test_reparacion_infraestructura(colonia_prueba):
    granja = Granja(eficiencia=100)
    for _ in range(10):
        granja.aplicar_efecto(colonia_prueba)

    assert granja.eficiencia == 0

    recursos_escasos = {"Madera": 2, "Agua": 5}
    assert granja.reparar(recursos_escasos) is False
    assert granja.eficiencia == 0

    recursos_para_reparar = {"Madera": 10, "Agua": 20}
    assert granja.reparar(recursos_para_reparar) is True
    assert granja.eficiencia == 100
    assert recursos_para_reparar["Madera"] == 3
    assert recursos_para_reparar["Agua"] == 3

def test_validaciones_setters():
    granja = Granja()

    with pytest.raises(ValueError):
        granja.eficiencia = 150

    with pytest.raises(ValueError):
        granja.eficiencia = -10

    with pytest.raises(TypeError):
        granja.eficiencia = "alta"

    with pytest.raises(ValueError):
        Infraestructura("BaseLunar")

    with pytest.raises(TypeError):
        Infraestructura(123)