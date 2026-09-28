class Colono():
    def __init__(self, nombre: str, nombre_colonia: str, edad: int, nivel: int, genero: str):
        self.nombre = nombre
        self.nombre_colonia = nombre_colonia
        self.edad = edad
        self.nivel = nivel
        self.genero = genero

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
        if genero != "M" or genero != "F":
            raise ValueError("Genero invalido")
        self._genero = genero
    
    def subir_nivel(self):
        self.nivel += 1

    def envejecer(self):
        self.edad += 1
