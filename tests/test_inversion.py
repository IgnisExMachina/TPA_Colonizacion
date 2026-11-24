import pytest
from Infraestructura.Aserradero import Aserradero
from Infraestructura.Infraestructura import Infraestructura


class ColoniaTest:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.recursos = {}


@pytest.fixture
def recursos_abundantes():
    return {"Madera": 1000, "Piedra": 1000, "Agua": 1000, "Hierro": 1000}


def test_invertir_sube_nivel_y_descuenta(recursos_abundantes):
    aserradero = Aserradero()
    coste = aserradero.coste_inversion()

    assert aserradero.invertir(recursos_abundantes) is True
    assert aserradero.nivel == 2
    for recurso, cantidad in coste.items():
        assert recursos_abundantes[recurso] == 1000 - cantidad


def test_invertir_deja_eficiencia_al_100(recursos_abundantes):
    aserradero = Aserradero(eficiencia=30)
    aserradero.invertir(recursos_abundantes)
    assert aserradero.eficiencia == 100


def test_coste_inversion_crece_con_el_nivel(recursos_abundantes):
    aserradero = Aserradero()
    coste_nv1 = aserradero.coste_inversion()
    aserradero.invertir(recursos_abundantes)
    coste_nv2 = aserradero.coste_inversion()
    assert all(coste_nv2[r] > coste_nv1[r] for r in coste_nv1)


def test_invertir_sin_recursos_no_hace_nada():
    aserradero = Aserradero()
    recursos = {"Madera": 0, "Piedra": 0}
    assert aserradero.invertir(recursos) is False
    assert aserradero.nivel == 1
    assert recursos == {"Madera": 0, "Piedra": 0}


def test_no_se_pasa_del_nivel_maximo(recursos_abundantes):
    aserradero = Aserradero()
    for _ in range(Infraestructura.MAX_NIVEL + 3):
        aserradero.invertir(recursos_abundantes)
    assert aserradero.nivel == Infraestructura.MAX_NIVEL
    assert aserradero.puede_invertir() is False


def test_multiplicador_aumenta_la_produccion(recursos_abundantes):
    colonia = ColoniaTest("Alfa")
    aserradero = Aserradero()
    aserradero.aplicar_efecto(colonia)
    produccion_nv1 = colonia.recursos["Madera"]

    aserradero.invertir(recursos_abundantes)  # nivel 2 y eficiencia 100
    colonia.recursos["Madera"] = 0
    aserradero.aplicar_efecto(colonia)
    assert colonia.recursos["Madera"] > produccion_nv1
    assert aserradero.multiplicador() == 1.5


def test_reparar_usa_la_mitad_del_coste():
    aserradero = Aserradero(eficiencia=0)
    coste = aserradero.coste_reparacion()
    recursos = dict(coste)  # justo lo necesario
    assert aserradero.reparar(recursos) is True
    assert aserradero.eficiencia == 100
    assert all(cantidad == 0 for cantidad in recursos.values())


def test_desgaste_no_baja_de_cero():
    colonia = ColoniaTest("Alfa")
    aserradero = Aserradero(eficiencia=5)  # una averia puede dejarla asi
    aserradero.aplicar_efecto(colonia)
    assert aserradero.eficiencia == 0


def test_infraestructura_cargada_de_partida_puede_invertir(tmp_path, recursos_abundantes):
    # Antes, las infraestructuras cargadas del JSON no tenian coste y "Invertir" daba AttributeError
    from GestorPersistencia import GestorPersistencia
    from Infraestructura.Granja import Granja

    gestor = GestorPersistencia(tmp_path / "partida.json")
    gestor.guardar_colonias([Granja()])
    granja = gestor.cargar_colonias()[0]

    assert granja.coste == Infraestructura.COSTES["Granja"]
    assert granja.invertir(recursos_abundantes) is True
    assert granja.coste_reparacion()
