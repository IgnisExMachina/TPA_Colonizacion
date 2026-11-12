
class Evento:
    Titulos = {
        #TORMENTAS: consumen recursos
        ("tormenta", 1) : "Llovizna",
        ("tormenta", 2) : "Chubascos",
        ("tormenta", 3) : "Tormenta",
        ("tormenta", 4) : "Tormenta Tropical",
        ("tormenta", 5) : "Huracán",
        #ENEMIGOS: matan a x colonos. x = severidad (1 - 5)
        ("enemigos", 1): "Escaramuza",
        ("enemigos", 2): "Incursión",
        ("enemigos", 3): "Ataque",
        ("enemigos", 4): "Asedio",
        ("enemigos", 5): "Invasión",
        #VISITAS: se unen directamente a la colonia
        ("visitas", 1): "Peregrinos",
        ("visitas", 2): "Viajeros",
        ("visitas", 3): "Caravana",
        ("visitas", 4): "Delegación",
        ("visitas", 5): "Festival", #No se como llamarlo se admiten sugerencias
        #AVERIAS: afectan a las infraestructuras de la colonia. si la colonia no tiene infraestructuras, no hace nada
        ("averia", 1): "Apagón",
        ("averia", 2): "Mantenimiento",
        ("averia", 3): "Fallo",
        ("averia", 4): "Fallo Estructural",
        ("averia", 5): "Fallo Total",
        ("desastre", 5): "Meteorito", #ELIMINA la colonia. Cuando se implemente la interpretacion de los eventos, si sale Meteorito, probabilidad de 9/10(por ejemplo) de sacar otro evento y no el meteorito 
        #probabilidad real del meteorito seria 1/21 x 1/9 = ~0.52%
    }
    def __init__(self, tipo: str, severidad: int): #severidad: cuanto impacto tiene el evento
        self.tipo = tipo
        self.severidad = severidad

    @property
    def titulo(self) -> str:
        return Evento.Titulos.get((self.tipo, self.severidad), "Evento Desconocido")

    def __repr__(self):
        return f"Evento: {self.titulo}(tipo={self.tipo}, severidad={self.severidad})"

