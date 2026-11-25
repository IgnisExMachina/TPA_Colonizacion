from Infraestructura import Infraestructura

class NaveEspacial(Infraestructura.Infraestructura):
    nTripulacion = 5
    def __init__(self, eficiencia: int = 100):
        super().__init__(tipo="NaveEspacial", eficiencia=eficiencia)
        self.modificador = (self.eficiencia / 100) / self.multiplicador()
        self.tripulacion = []
        self.requisitos = {"Plantas" : 0, "Plutonio": 0}

    #! No sobreescribimos aplicar_efecto. a cada golpe de reloj pierde eficiencia y no genera recursos -> requiere mantenimiento

    def listo_para_despegue(self, colonia):
        self.modificador = (self.eficiencia/100) / self.multiplicador()
        if len(self.tripulacion) == NaveEspacial.nTripulacion:
            if self.requisitos["Plantas"] >= 20 * self.modificador or self.requisitos["Plutonio"] >= 30 * self.modificador:
                return True
        else:
            return False
        return False

    def agregar_a_tripulacion(self, colono): #todo: logica de seleccion tiene que ir donde se llamen las funciones
        self.tripulacion.append(colono)

    def agregar_requisitos(self, recursos: dict):
        if recursos["Plantas"] < 20 * self.modificador:
            self.requisitos["Plantas"] += recursos["Plantas"]
            recursos["Plantas"] = 0
        else:
            self.requisitos["Plantas"] += 20 * self.modificador
            recursos["Plantas"] -= 20 * self.modificador

        if recursos["Plutonio"] < 30 * self.modificador:
            self.requisitos["Plutonio"] += recursos["Plutonio"]
            recursos["Plutonio"] = 0
        else:
            self.requisitos["Plutonio"] += 30 * self.modificador
            recursos["Plutonio"] -= 30 * self.modificador

        
