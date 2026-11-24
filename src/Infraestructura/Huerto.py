import random

from Infraestructura import Infraestructura

class Huerto(Infraestructura.Infraestructura):
    PARCELAS = 6              # parcelas a nivel 1 (cada nivel invertido suma PARCELAS_POR_NIVEL)
    PARCELAS_POR_NIVEL = 2
    EVENTOS_PARA_CRECER = 5   # eventos que tiene que pasar una semilla para poder recogerse
    MAX_SEMILLAS_POR_PLANTA = 2

    def __init__(self, eficiencia: int = 100, plantas: list = None):
        super().__init__(tipo="Huerto", eficiencia=eficiencia)
        # Cada elemento es una planta y su valor son los eventos que lleva creciendo.
        # Es una lista de enteros para que el GestorPersistencia la guarde sin problemas.
        self.plantas = plantas if plantas is not None else []

    # --- Consultas ---
    def esta_madura(self, eventos_crecidos: int) -> bool:
        return eventos_crecidos >= self.EVENTOS_PARA_CRECER

    def plantas_maduras(self) -> int:
        return sum(1 for p in self.plantas if self.esta_madura(p))

    def num_parcelas(self) -> int:
        return self.PARCELAS + self.PARCELAS_POR_NIVEL * (self.nivel - 1)

    def descripcion_mejora(self) -> str:
        return f"{self.num_parcelas()} parcelas"

    def parcelas_libres(self) -> int:
        return self.num_parcelas() - len(self.plantas)

    # --- Acciones ---
    def plantar(self, colonia) -> bool:
        if self.parcelas_libres() <= 0:
            print(f"El Huerto de {colonia.nombre} está lleno.")
            return False
        if colonia.recursos.get("Semillas", 0) < 1:
            print(f"{colonia.nombre} no tiene semillas. Envía a un colono de exploración.")
            return False

        colonia.recursos["Semillas"] -= 1
        self.plantas.append(0)
        print(f"Se ha plantado una semilla en el Huerto de {colonia.nombre}.")
        return True

    def recoger(self, colonia) -> dict:
        """Recoge todas las plantas maduras. Cada una da 1 Planta y entre 0 y 2 Semillas nuevas."""
        maduras = self.plantas_maduras()
        if maduras == 0:
            print(f"No hay plantas listas para recoger en {colonia.nombre}.")
            return {"Plantas": 0, "Semillas": 0}

        semillas = sum(random.randint(0, self.MAX_SEMILLAS_POR_PLANTA) for _ in range(maduras))
        self.plantas = [p for p in self.plantas if not self.esta_madura(p)]

        colonia.recursos["Plantas"] = colonia.recursos.get("Plantas", 0) + maduras
        colonia.recursos["Semillas"] = colonia.recursos.get("Semillas", 0) + semillas
        print(f"Cosecha en {colonia.nombre}: {maduras} planta(s) y {semillas} semilla(s).")
        return {"Plantas": maduras, "Semillas": semillas}

    def aplicar_efecto(self, colonia):
        # Cada evento que pasa, las plantas crecen un paso
        if not super().aplicar_efecto(colonia):
            return
        self.plantas = [p + 1 for p in self.plantas]
        print(f"Las plantas del Huerto de {colonia.nombre} crecen ({self.plantas_maduras()}/{len(self.plantas)} listas). Eficiencia: {self.eficiencia}")
