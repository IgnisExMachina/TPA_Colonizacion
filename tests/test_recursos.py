import pytest
from Recursos import Recursos

@pytest.fixture
def recurso_madera():
    return Recursos(tipo="Madera", cantidad=50) 

def test_creacion_recurso():
    recurso = Recursos(tipo="Piedra", cantidad=30)
    assert recurso.tipo == "Piedra"
    assert recurso.cantidad == 30

def test_setter_tipo_valido(recurso_madera):
    recurso_madera.tipo = "Piedra" 
    assert recurso_madera.tipo == "Piedra"

def test_setter_tipo_invalido(recurso_madera):
    with pytest.raises(ValueError):
        recurso_madera.tipo = "Oro"

    with pytest.raises(ValueError):
        recurso_madera.tipo = "123"

def test_setter_cantidad_invalida(recurso_madera):
    with pytest.raises(ValueError):
        recurso_madera.cantidad = -5

    with pytest.raises(ValueError):
        recurso_madera.cantidad = "diez"