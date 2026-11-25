import random

class Colono():
    NOMBRES = {
        "NOMBRE" : ["María Carmen", "Antonio", "María", "Manuel", "José", "Francisco", "David", "Carmen", "Daniel", "Javier", "Juan", "José Antonio", "Francisco Javier", "Carlos", "Alejandro", "José Luis", "Ana María", "Jesús", "Laura", "María Pilar"],
        "APELLIDO" : ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Hernández", "Ruiz", "Díaz", "Moreno", "Muñoz", "Álvarez", "Romero", "Gutiérrez", "Alonso"]
    }
    EVENTOS_EXPLORACION = 5  # eventos que tarda un colono en volver de explorar

    @classmethod
    def aleatorio(cls, nombre_colonia: str) -> "Colono":
        """Crea un colono con nombre, edad, nivel y genero al azar."""
        nombre = f"{random.choice(cls.NOMBRES['NOMBRE'])} {random.choice(cls.NOMBRES['APELLIDO'])}"
        return cls(nombre=nombre, nombre_colonia=nombre_colonia, edad=random.randint(18, 80),
                   nivel=random.randint(1, 10), genero=random.choice(["M", "F"]))

    def __init__(self, nombre: str, nombre_colonia: str, edad: int, nivel: int, genero: str,):
        self.nombre = nombre
        self.nombre_colonia = nombre_colonia
        self.edad = edad
        self.nivel = nivel
        self.genero = genero
        self.ocupado = False
        self.exploracion_restante = 0  # eventos que faltan para volver de explorar (0 = en la colonia)

    @property
    def nombre(self):
        return self._nombre

    @property
    def nombre_colonia(self):
        return self._nombre_colonia

    @property
    def edad(self):
        return self._edad

    @property
    def nivel(self):
        return self._nivel

    @property
    def genero(self):
        return self._genero

    @property
    def ocupado(self):
        return self._ocupado

    @nombre.setter
    def nombre(self, nombre: str):
        if not nombre:
            raise ValueError("El nombre no puede estar vacio")
        self._nombre = nombre

    @nombre_colonia.setter
    def nombre_colonia(self, nombre_colonia: str):
        if not nombre_colonia:
            raise ValueError("El nombre de la colonia no puede estar vacio")
        self._nombre_colonia = nombre_colonia

    @edad.setter
    def edad(self, edad: int):
        if edad < 0:
            raise ValueError("La edad debe ser positiva")
        self._edad = edad

    @nivel.setter
    def nivel(self, nivel: int):
        if nivel < 0:
            raise ValueError("El nivel debe ser positivo")
        self._nivel = nivel

    @genero.setter
    def genero(self, genero: str):
        if genero != "M" and genero != "F":
            raise ValueError("Genero invalido")
        self._genero = genero

    @ocupado.setter
    def ocupado(self, ocupado: bool):
        self._ocupado = ocupado

    def __str__(self):
        return f"Nombre: {self.nombre}\nColonia: {self.nombre_colonia}\nEdad: {self.edad}\nNivel: {self.nivel}\nGenero: {'Masculino' if self.genero == 'M' else 'Femenino'}\nOcupado? {'Si' if self.ocupado else 'No'}"

    def subir_nivel(self):
        self.nivel += 1

    def envejecer(self):
        self.edad += 1

    def irDeExploracion(self, colonia) -> bool:
        """El colono sale a explorar. Tarda EVENTOS_EXPLORACION eventos en volver y,
        al volver, trae lo que haya encontrado (de momento solo semillas)."""
        if self.ocupado:
            print(f"{self.nombre} está ocupado y no puede ir de exploración.")
            return False
        self.ocupado = True
        self.exploracion_restante = self.EVENTOS_EXPLORACION
        print(f"{self.nombre} sale de exploración desde {colonia.nombre}. Volverá en {self.EVENTOS_EXPLORACION} eventos.")
        return True

    def esta_explorando(self) -> bool:
        # getattr por si el colono viene de una partida guardada antes de existir este atributo
        return getattr(self, "exploracion_restante", 0) > 0

    RECURSOS_EXPLORACION = ["Madera", "Agua", "Piedra", "Semilla"]

    def avanzar_exploracion(self, colonia) -> dict | None:
        """Se llama en cada evento. Devuelve los hallazgos cuando el colono vuelve, si no None."""
        if not self.esta_explorando():
            return None
        self.exploracion_restante -= 1
        if self.exploracion_restante > 0:
            return None

        # Vuelve de la exploracion. Cuanto mas nivel, mas probable es que encuentre algo.
        hallazgos = {"Semillas" : 0}
        intentos = 1 + self.nivel // 4   # nivel 1-3: 1 intento, 4-7: 2, 8+: 3...
        for _ in range(intentos):
            hallazgos["Semillas"] += random.randint(0, 2)
            recurso = random.choice(self.RECURSOS_EXPLORACION)
            cantidad = random.randint(0,5)
            if cantidad > 0:
                hallazgos[recurso] = hallazgos.get(recurso, 0) + cantidad

        for recurso, cantidad in hallazgos.items():
            colonia.recursos[recurso] = colonia.recursos.get(recurso, 0) + cantidad

        self.ocupado = False

        partes = []
        for recurso, cantidad in hallazgos.items():
            if cantidad > 0:
                partes.append(f"{cantidad} de {recurso.lower()}")

        if partes:
            print(f"{self.nombre} vuelve de explorar con {', '.join(partes)}.")
        else:
            print(f"{self.nombre} vuelve de explorar sin encontrar nada.")
        return hallazgos
