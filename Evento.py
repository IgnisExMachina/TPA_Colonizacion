
class Evento:
    Titulos = {
        ("tormenta", 1) : "Llovizna",
        ("tormenta", 2) : "Chubascos",
        ("tormenta", 3) : "Tormenta",
        ("tormenta", 4) : "Tormenta Tropical",
        ("tormenta", 5) : "Huracán",
        ("enemigos", 1): "Escaramuza",
        ("enemigos", 2): "Incursión",
        ("enemigos", 3): "Ataque",
        ("enemigos", 4): "Asedio",
        ("enemigos", 5): "Invasión",
    }
    def __init__(self, tipo: str, severidad: int): #severidad: cuanto impacto tiene el evento
        self.tipo = tipo
        self.severidad = severidad

    @property
    def titulo(self) -> str:
        return Evento.Titulos.get((self.tipo, self.severidad), "Evento Desconocido")

    def __repr__(self):
        return f"Evento: {self.titulo}(tipo={self.tipo}, severidad={self.severidad})"

