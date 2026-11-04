class Recursos () :
    RECURSOS = {
        "Madera" : {"Puente": 20, "Granja" : 15},
        "Piedra" : {"Puente" : 10 , "Castillo" : 50 , "Muralla": 30},
        "Agua"   : {"Castillo" : 20 , "Granja" : 35} ,
        "Hierro" : {"Castillo": 30}
    }

# ? RAREZAS : Común, Raro, Escaso
    def __init__(self, tipo: str, cantidad : int):
        self.cantidad = cantidad
        self.tipo = tipo

    @property
    def tipo (self) :
        return self._tipo

    @property
    def cantidad (self) :
        return self._cantidad
    

    @tipo.setter         
    def tipo (self, tipo : str) :
        if not isinstance (tipo, str) :
            raise ValueError(f"El recurso debe ser una cadena de texto.")
        if tipo in self.RECURSOS:
            self._tipo = tipo
        else :
            raise ValueError(f"El recurso {tipo} no es valido. Opciones: {list(self.RECURSOS.keys())}")

    @cantidad.setter 
    def cantidad (self, cantidad) :
        if not isinstance (cantidad, int) :
            raise ValueError(f"La cantidad debe ser un numero.")
        if cantidad < 0 :
            raise ValueError ("La cantidad no puede ser negativa")
        self._cantidad = cantidad

    def mostrar_recursos (self) :
        print (f"Con {self.tipo} (Rareza: {self.rareza}) puedes construir: ")
        for infra, coste in self.RECURSOS [self.tipo].items () :
            print (f"\t{infra} | {coste}")

