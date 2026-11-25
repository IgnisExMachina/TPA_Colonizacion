from Infraestructura import Infraestructura

class NaveEspacial(Infraestructura.Infraestructura): 
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="NaveEspacial", eficiencia=eficiencia)
        self.tripulacion = None
        self.requisitos = {"Plantas" : 0, "Plutonio": 0}
    #! No sobreescribimos aplicar_efecto. a cada golpe de reloj pierde eficiencia y no genera recursos -> requiere mantenimiento

    def listo_para_despegue(self, colonia):
        modificador = (self.eficiencia/100) / self.multiplicador()
        if len(self.tripulacion) == 5:
            if self.requisitos["Plantas"] >= 20 * modificador and self.requisitos["Plutonio"] >= 30:
                return True
        else:
            return False

    def añadir_a_tripulacion(self, colono): #todo: logica de seleccion tiene que ir donde se llamen las funciones
        self.tripulacion.append(colono)

        
