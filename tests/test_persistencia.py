import json
from pathlib import Path
import pytest
from GestorPersistencia import GestorPersistencia
from Colonia import Colonia
from Colono import Colono
from Infraestructura.Granja import Granja
from Infraestructura.Mina import Mina


@pytest.fixture
def ruta_json_temporal():
    ruta = Path("tests/temp_colonias_test.json")
    yield ruta
    if ruta.exists():
        ruta.unlink()


def test_guardar_y_cargar_colonias(ruta_json_temporal):
    gestor = GestorPersistencia(str(ruta_json_temporal))

    colono = Colono("Elena", "Alfa", 24, 2, "F")
    granja = Granja(eficiencia=80)
    mina = Mina(eficiencia=90)

    colonia_original = Colonia(
        nombre="Alfa",
        colonos=[colono],
        infraestructuras=[granja, mina],
        recursos={"Madera": 40, "Agua": 55}
    )

    colonias_cargadas = {}
    try:
        gestor.guardar_colonias({"Alfa": colonia_original})
        assert ruta_json_temporal.exists()

        colonias_cargadas = gestor.cargar_colonias()
        assert "Alfa" in colonias_cargadas

        colonia_recuperada = colonias_cargadas["Alfa"]
        assert isinstance(colonia_recuperada, Colonia)
        assert colonia_recuperada.nombre == "Alfa"
        assert colonia_recuperada.recursos["Madera"] == 40
        assert colonia_recuperada.recursos["Agua"] == 55

        #verificamos si reconstruye el objeto Colono
        assert len(colonia_recuperada.colonos) == 1
        assert isinstance(colonia_recuperada.colonos[0], Colono)
        assert colonia_recuperada.colonos[0].nombre == "Elena"
        assert colonia_recuperada.colonos[0].nivel == 2

        #verificamos si reconstruye las infraestructuras con su eficiencia
        assert len(colonia_recuperada.infraestructuras) == 2
        assert isinstance(colonia_recuperada.infraestructuras[0], Granja)
        assert colonia_recuperada.infraestructuras[0].eficiencia == 80
        assert isinstance(colonia_recuperada.infraestructuras[1], Mina)
        assert colonia_recuperada.infraestructuras[1].eficiencia == 90
    finally:
        colonia_original.detener_gestion()
        for col in colonias_cargadas.values():
            col.detener_gestion()


def test_cargar_archivo_inexistente(ruta_json_temporal):
    gestor = GestorPersistencia(str(ruta_json_temporal))

    with pytest.raises(FileNotFoundError):
        gestor.cargar_colonias()


def test_cargar_archivo_corrupto(ruta_json_temporal):
    ruta_json_temporal.write_text("{ esto no es un json valido", encoding="utf-8")
    gestor = GestorPersistencia(str(ruta_json_temporal))

    with pytest.raises(ValueError):
        gestor.cargar_colonias()


def test_cargar_clase_desconocida(ruta_json_temporal):
    datos_invalidos = {"__clase__": "NaveEspacial", "nombre": "Enterprise"}
    ruta_json_temporal.write_text(json.dumps(datos_invalidos), encoding="utf-8")
    gestor = GestorPersistencia(str(ruta_json_temporal))

    with pytest.raises(ValueError):
        gestor.cargar_colonias()