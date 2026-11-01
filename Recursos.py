class Recursos () :
    RECURSOS = {
        "Madera" : {"Puente": 20, "Granja" : 15},
        "Piedra" : {"Puente" : 10 , "Castillo" : 50 , "Muralla": 30},
        "Agua"   : {"Castillo" : 20 , "Granja" : 35} ,
        "Hierro" : {"Castillo": 30}
    }

    def __init__(self, rareza : str , cantidad : int, tipo : str):
        self.rareza = rareza
        self.cantidad = cantidad
        self.tipo = tipo

    @property
    def rareza (self) :
        return self._rareza

    @property
    def tipo (self) :
        return self._tipo

    @property
    def cantidad (self) :
        return self._cantidad
    
    @rareza.setter         
    def rareza (self, rareza) :
        if not isinstance (rareza, str) :
            raise ValueError(f"La rareza debe ser una cadena de texto.")
        self._rareza = rareza

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

