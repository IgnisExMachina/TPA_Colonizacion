from infraestructura import Infraestructura

class Recurso () :
    RECURSOS = {
        "Madera" : {"Puente": 20, "Granja" : 15},
        "Piedra" : {"Puente" : 10 , "Castillo" : 50 , "Muralla": 30},
        "Agua"   : {"Castillo" : 20 , "Granja" : 35} ,
        "Hierro" : {"Castillo": 30}
    }

    def __init__(self, rareza : str , cantidad : int, tipo : str): # Falta agregar Aplicacion
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
        self._rareza = rareza

    @rareza.setter         
    def tipo (self, tipo) :
        self._tipo = tipo

    @cantidad.setter 
    def cantidad (self, cantidad) :
        if cantidad < 0 :
            raise ValueError ("La cantidad no puede ser negativa")
        else :
            self._cantidad = cantidad

    def mostrar_recursos (self) :
        print (f"Con {self.tipo} puedes construir: ")
        for infra, coste in self.RECURSOS [self.tipo].items () :
            print (f"\t{infra} | {coste}")

