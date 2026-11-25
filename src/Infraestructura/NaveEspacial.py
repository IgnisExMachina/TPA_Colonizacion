from Infraestructura import Infraestructura

class NaveEspacial(Infraestructura.Infraestructura):
    nTripulacion = 5
    self.modificador = (self.eficiencia / 100) / self.multiplicador()
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="NaveEspacial", eficiencia=eficiencia)
        self.tripulacion = []
        self.requisitos = {"Plantas" : 60, "Plutonio": 60}
        self.modificador = (self.eficiencia / 100) / self.multiplicador()
    #! No sobreescribimos aplicar_efecto. a cada golpe de reloj pierde eficiencia y no genera recursos -> requiere mantenimiento

    def listo_para_despegue(self, colonia):
        self.modificador = (self.eficiencia/100) / self.multiplicador()
        if len(self.tripulacion) == NaveEspacial.nTripulacion:
            if self.requisitos["Plantas"] >= 20 * modificador or self.requisitos["Plutonio"] >= 30 * modificador:
                return True
        else:
            return False
        return False

    def agregar_a_tripulacion(self, colono): #todo: logica de seleccion tiene que ir donde se llamen las funciones
        self.tripulacion.append(colono)

    def agregar_requisitos(self, recursos: dict):


        
