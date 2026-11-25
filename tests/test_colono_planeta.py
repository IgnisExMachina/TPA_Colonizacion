import pytest
from Colono import Colono
from Planeta import Planeta
from Colonia import Colonia


#Tests de Colono

def test_creacion_colono():
    colono = Colono("Elena", "Sociópatas", 22, 1, "F")
    assert colono.nombre == "Elena"
    assert colono.nombre_colonia == "Sociópatas"
    assert colono.edad == 22
    assert colono.nivel == 1
    assert colono.genero == "F"
    assert colono.ocupado is False

#esto comprueba todos los tipos de errores que pueden ocurrir al instanciar un colono
@pytest.mark.parametrize("nombre,colonia,edad,nivel,genero", [
    ("", "Kukusclan", 25, 1, "M"),         # nombre vacio
    ("Alfredo", "", 25, 1, "M"),           # colonia vacia
    ("Alfredo", "Kukusclan", -1, 1, "M"),  # edad negativa
    ("Alfredo", "Kukusclan", 25, -5, "M"), # nivel negativo
    ("Alfredo", "Kukusclan", 25, 1, "X"),  # genero invalido
])

def test_colono_setters(nombre, colonia, edad, nivel, genero):
    with pytest.raises(ValueError):
        Colono(nombre, colonia, edad, nivel, genero)

def test_colono_progresion():
    colono = Colono("Ruben", "La sociedad de la nieve", 30, 1, "M")
    colono.subir_nivel()
    colono.envejecer()
    colono.ocupado = True

    assert colono.nivel == 2
    assert colono.edad == 31
    assert colono.ocupado is True
    assert "Masculino" in str(colono)
    assert "Ocupado? Si" in str(colono)




#Tests de Planeta

def test_creacion_planeta():
    planeta = Planeta("   Marte  ")
    assert planeta.nombre == "Marte"
    assert planeta.colonia is None
    assert planeta.recursosDisponibles == {}


def test_planeta_nombre_vacio():
    with pytest.raises(ValueError):
        Planeta("")


def test_fundar_colonia_en_planeta():
    planeta = Planeta("Kepler-22b")
    colonia1 = Colonia("Kukusclan")
    colonia2 = Colonia("Sociopatas")

    planeta.fundarColonia(colonia1)
    assert planeta.colonia is colonia1

    with pytest.raises(ValueError):
        planeta.fundarColonia(colonia2)