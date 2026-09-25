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
        return self._nombre

    @property
    def genero(self):
        return self._genero

    @nombre.setter
    def nombre(self, nombre):
        #comprobar str no vacio
        self._nombre = nombre

    @nombre_colonia.setter
    def nombre_colonia(self, nombre_colonia):
        #comprobar str no vacio
        self._nombre_colonia = nombre_colonia

    @edad.setter
    def edad(self, edad):
        #comprobar str no vacio
        self._edad = edad

    @nivel.setter
    def nivel(self, nivel):
        #comprobar str no vacio
        self._nivel = nivel

    @genero.setter
    def genero(self, genero):
        #comprobar str no vacio
        self._genero = genero
    
    
    
