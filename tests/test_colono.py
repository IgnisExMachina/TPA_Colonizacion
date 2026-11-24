from Colono import Colono


class ColoniaTest:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.recursos = {"Semillas": 0}


def test_ir_de_exploracion_lo_deja_ocupado():
    colonia = ColoniaTest("Alfa")
    colono = Colono("Ana", "Alfa", 20, 1, "F")
    assert colono.irDeExploracion(colonia) is True
    assert colono.ocupado is True
    assert colono.exploracion_restante == Colono.EVENTOS_EXPLORACION


def test_no_puede_explorar_si_ya_esta_ocupado():
    colonia = ColoniaTest("Alfa")
    colono = Colono("Ana", "Alfa", 20, 1, "F")
    colono.irDeExploracion(colonia)
    assert colono.irDeExploracion(colonia) is False


def test_vuelve_tras_cinco_eventos_con_semillas():
    colonia = ColoniaTest("Alfa")
    colono = Colono("Ana", "Alfa", 20, 1, "F")
    colono.irDeExploracion(colonia)

    for _ in range(Colono.EVENTOS_EXPLORACION - 1):
        assert colono.avanzar_exploracion(colonia) is None
        assert colono.esta_explorando()

    hallazgos = colono.avanzar_exploracion(colonia)
    assert hallazgos is not None
    assert colono.ocupado is False
    assert not colono.esta_explorando()
    assert colonia.recursos["Semillas"] == hallazgos["Semillas"]


def test_colono_aleatorio_es_valido():
    colono = Colono.aleatorio("Alfa")
    assert colono.nombre_colonia == "Alfa"
    assert 18 <= colono.edad <= 80
    assert colono.genero in ("M", "F")
