from Colono import Colono

import Infraestructura

from eventos.GestorEventos import GestorEventos as Gestor
import sys
import threading
import queue
import random

class Colonia:
    destruida = False  # ? True tras un meteorito: el planeta queda libre (valor de clase para partidas antiguas)
    abandonada = False  # ? True si se quedo sin colonos ni infraestructuras: la colonia desaparece
    noFundada = False # ? True solo cuando se fuerza. Para colonias por defecto vacias y empezar el juego de 0
    RECURSOS_BASE = {"Madera": 50, "Piedra": 50, "Agua": 50, "Hierro": 20, "Comida": 20, "Plutonio": 0, "Semillas": 2, "Plantas": 0}
    def __init__(self, nombre: str = "-", colonos: list = None, recursos: dict = None, infraestructuras: list = None):
        self.nombre = nombre
        
        if colonos is None:
            self.colonos = []
        else:
            self.colonos = colonos

        if infraestructuras is None:
            self.infraestructuras = []
        else:
            self.infraestructuras = infraestructuras
        
        self.recursos = self.RECURSOS_BASE.copy()
        
        if recursos:
            for tipo, cantidad in recursos.items():
                self.recursos[tipo] = cantidad

        self.destruida = False
        self.inicializar_runtime()

    def inicializar_runtime(self):
        self._gestor = Gestor(queue.Queue())
        self._stream = self.iniciar_gestor()
        
        self._thread = None
        self._active = False
        # ? Aqui no se toca 'destruida': esto tambien se llama al cargar partida y las colonias muertas resucitarian

    def agregarColono(self, colono: Colono):
        self.colonos.append(colono)

    def verColonos(self): #! PONERLO MÁS BONITO CADA COLONO
        texto = ""
        if not self.colonos:
            return "No hay colonos en este planeta."
        for colono in self.colonos:
            texto += f"{colono}\n"
        return texto

    def agregarRecurso(self, tipo: str, cantidad: int):
        if tipo in self.recursos :
            self.recursos[tipo] += cantidad
            print(f"Se han añadido {cantidad} de {tipo}. Total: {self.recursos[tipo]}")
        else:
            print(f"Error: El recurso {tipo} no existe en el sistema.")

    def consumirRecurso(self, tipo: str, cantidad: int):
        if tipo in self.recursos and self.recursos[tipo] >= cantidad:
            self.recursos[tipo] -= cantidad
            print(f"Se han consumido {cantidad} de {tipo}. Restante: {self.recursos[tipo]}")
            return
        print(f"Error: No hay suficientes recursos de {tipo} o el recurso no existe.")

    def verRecursos(self):
        if not self.recursos:
            print("No hay recursos todavía")
            return
        for tipo, cantidad in self.recursos.items():
            print(f"- {tipo}: {cantidad}")

    def agregarInfraestructuras(self, infraestructura: Infraestructura.Infraestructura):
        if infraestructura.construir(recursos_colonia=self.recursos):
            self.infraestructuras.append(infraestructura)

    def crear_infraestructuras(self, tipo):
        match tipo:
            case "Castillo":
                return self.agregarInfraestructuras(Infraestructura.Castillo())
            case "Granja":
                return self.agregarInfraestructuras(Infraestructura.Granja())
            case "Mina":
                return self.agregarInfraestructuras(Infraestructura.Mina())
            case "Muralla":
                return self.agregarInfraestructuras(Infraestructura.Muralla())
            case "Aserradero":
                return self.agregarInfraestructuras(Infraestructura.Aserradero())
            case "Pozo":
                return self.agregarInfraestructuras(Infraestructura.Pozo())
            case "ExtractorDePlutonio":
                return self.agregarInfraestructuras(Infraestructura.ExtractorDePlutonio())
            case "Huerto":
                return self.agregarInfraestructuras(Infraestructura.Huerto())
            case "NaveEspacial":
                return self.agregarInfraestructuras(Infraestructura.NaveEspacial())

    def obtener_huerto(self):
        """Devuelve el primer Huerto de la colonia o None si no tiene."""
        for infraestructura in self.infraestructuras:
            if isinstance(infraestructura, Infraestructura.Huerto):
                return infraestructura
        return None

    def verInfraestructuras(self):
        for infraestructura in self.infraestructuras:
            print(infraestructura.tipo)
            print(infraestructura.eficiencia)

    @property 
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str):
        self._nombre = nombre

    def iniciar_gestor(self):
        self._gestor.iniciar()
        try:
            while True:
                yield self._gestor.eventos_env.get()   
        except KeyboardInterrupt:
            self._gestor.detener()

    def procesar_eventos(self):
        self._active = True
        while self._active:
            evento = next(self._stream)
            try:
                self._aplicar_evento(evento)
            except Exception as e:
                # ? Un fallo en un evento no puede dejar a la colonia sin eventos para siempre
                # ? A stderr: se ve en la terminal pero no en el registro de la app
                print(f"Error procesando el evento {evento} en {self.nombre}: {e!r}", file=sys.stderr)

    def _aplicar_evento(self, evento):
        print(self.nombre)
        match evento.tipo:
            case "tormenta":
                print(f"{evento.titulo}!")
                for tipo in list(self.recursos):  # copia: otro hilo puede añadir recursos
                    cantidad = min(evento.severidad, self.recursos[tipo])
                    if cantidad > 0:
                        self.consumirRecurso(tipo=tipo, cantidad=cantidad)
            case "enemigos":
                for i in range(evento.severidad):
                    # Los que estan explorando estan fuera de la colonia y se libran
                    en_colonia = [c for c in self.colonos if not c.esta_explorando()]
                    if not en_colonia:
                        break
                    victima = en_colonia[-1]
                    self.colonos.remove(victima)
                    print(f"{evento.titulo}! {victima.nombre} muere en combate")
            case "visitas":
                print(f"{evento.severidad} colono(s) se unen a la colonia!")
                for i in range(evento.severidad):
                    self.agregarColono(Colono.aleatorio(self.nombre))
            case "averia":
                if self.infraestructuras:
                    averiado = random.choice(self.infraestructuras)
                    if evento.severidad == 1 or evento.severidad == 2:
                        averiado.eficiencia = int(averiado.eficiencia * 1/2)
                    elif evento.severidad == 3 or evento.severidad == 4:
                        averiado.eficiencia = int(averiado.eficiencia * 1/4)
                    else:
                        self.infraestructuras.remove(averiado)
                    print(f"{evento.titulo} afecta a la infraestructura {averiado.tipo}")
            case "desastre":
                print("Impacto de meteorito. Colonia destruida.")
                self.colonos.clear()
                self.infraestructuras.clear()
                self.recursos.clear()
                self.destruida = True
                self.detener_gestion()
                return
        for infraestructura in list(self.infraestructuras):
            infraestructura.aplicar_efecto(self)
        for colono in list(self.colonos):
            colono.avanzar_exploracion(self)

    def iniciar_gestion(self):
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(target=self.procesar_eventos, daemon=True)
            self._thread.start()
            print(f"Colonia '{self.nombre}' iniciada en paralelo.")

    def detener_gestion(self):
        self._active = False
        try:
            self._gestor.detener()
        except Exception:
            pass