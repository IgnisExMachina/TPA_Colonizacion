class RecursosDelPlaneta:
    def __init__(self, tipo : str, cantidad: int, cantidadMaxima: int):
        self.tipo = tipo
        self.cantidad = cantidad
        self.cantidadMaxima = cantidadMaxima

    @property #getter
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo: str):
        self._tipo = tipo

    @property #getter
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, cantidad: str):
        self._cantidad = cantidad

    @property #getter
    def cantidadMaxima(self):
        return self._cantidadMaxima

    @cantidadMaxima.setter
    def cantidadMaxima(self, cantidadMaxima: str):
        self._cantidadMaxima = cantidadMaxima


    def extraer(self, cantidadParaExtraer):
        if cantidadParaExtraer <= 0 :
            raise ValueError("La cantidad para extraer debe ser mayor a 0!")