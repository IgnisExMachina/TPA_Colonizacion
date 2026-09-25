class Recursos () :

    def __init__(self, rareza : str , cantidad : int): # Falta agregar Aplicacion

        self.rareza = rareza
        self.cantidad = cantidad


    @property
    
    def rareza (self) :
    
        return self._rareza
    
    @rareza.setter 
            
    def rareza (self, rareza) :
            
        self._rareza = rareza


    @property

    def cantidad (self) :

        return self._cantidad

    
    @cantidad.setter 
        
    def cantidad (self, cantidad) :
        
        if cantidad < 0 :

            raise ValueError ("La cantidad no puede ser negativa")
        
        else :
            
            self._cantidad = cantidad
