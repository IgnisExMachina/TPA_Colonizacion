import tkinter as tk

import Infraestructura
from Colonia import Colonia
from interfaz.VentanaFundar import VentanaFundar
from Infraestructura.NaveEspacial import NaveEspacial
from interfaz import Tema
import random

class VentanaNave:
    def __init__(self, ventana_padre, colonia: Colonia, nave: Infraestructura.NaveEspacial, colonias: dict):
        self.colonia = colonia
        self.colonias = colonias
        self.nave = nave
        self._id_refresco = None
        self._planetasVacios = self.encontrar_planetas_vacios()
        self.ventanaPadre = ventana_padre

        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title(f"Nave de {colonia.nombre}")
        self.ventana.resizable(False, False)  # ? Evitamos que el usuario pueda ajustar la ventana
        self.ventana.configure(bg=Tema.FONDO)  # ? Pone tema de la ventana con lo que tenemos en el archivo Tema.py
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.botones = tk.Frame(self.ventana)
        self.botones.pack(pady=(0, 10))

        self.seleccion_planeta()
        # ? El frame crea un "div" donde irán los botones

    def seleccion_planeta(self):
        if self._planetasVacios:
            for key in self._planetasVacios:
                tk.Button(self.botones, text=f"Colonizar planeta {key}", command= lambda : self.colonizar(key)).pack(side=tk.LEFT, padx=5)
            tk.Button(self.botones, text="Cerrar", command=self.cerrar).pack(side=tk.LEFT, padx=5)
        else:
            print("ERROR: No hay planetas vacios.")

    def colonizar(self, key):
        self.popular_tripulacion()
        self.cargar()
        if not self.nave.listo_para_despegue(self.colonia):
            print("NO HAY SUFICIENTES RECURSOS")
            return None
        VentanaFundar(self.ventanaPadre, self.colonias, key, self.nave.tripulacion)
        self.colonia.infraestructuras.remove(self.nave)
        self.cerrar()

    def popular_tripulacion(self):
        aPopular = NaveEspacial.nTripulacion - len(self.nave.tripulacion)
        for i in range(aPopular):
            tripulante = random.choice(self.colonia.colonos)
            self.nave.agregar_a_tripulacion(tripulante)
            print(f"{tripulante.nombre} se una a la tripulación! No podrá ser enviado a explorar.")
        for colono in self.nave.tripulacion:
            if colono in self.colonia.colonos:
                self.colonia.colonos.remove(colono)

    def cargar(self):
        self.nave.agregar_requisitos(self.colonia.recursos)

    def cerrar(self):
        if self._id_refresco is not None:
            self.ventana.nametowidget(".").after_cancel(self._id_refresco)
            self._id_refresco = None
        self.ventana.destroy()

    #Utilidades
    def encontrar_planetas_vacios(self):
        vacios = {}
        for key in self.colonias:
            if not self.colonias[key] or self.colonias[key].destruida or self.colonias[key].noFundada:
                vacios[key] = self.colonias[key]
        return vacios
