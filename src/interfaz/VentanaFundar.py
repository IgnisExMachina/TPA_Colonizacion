import tkinter as tk
from Colonia import Colonia
import Infraestructura

class VentanaFundar():
    def __init__(self, ventanaPadre, coloniasExistentes, key):
        if coloniasExistentes == None:
            #si no hay ninguna, se crea una por defecto
            #self.fundar_colonia()
            print("Lameme las bolas")
        else:
            self.coloniasExistentes = coloniasExistentes
        self.ventana = tk.Toplevel(ventanaPadre)
        self.ventana.title("Planeta no ocupado.")
        self.ventana.geometry("400x400")
        self.key = key

        self.ventana.columnconfigure(1, weight=1)

        self.campos = {
            "Nombre Colonia": "NOMBRE",
            "Recursos adicionales": 0,
        }
        self.entradas = {}

        for fila, campo in enumerate(self.campos):
            label = tk.Label(self.ventana, text=f"{campo}:")
            label.grid(row=fila, column=0, padx=10, pady=8, sticky="w")

            entrada = tk.Entry(self.ventana)
            entrada.grid(row=fila, column=1, padx=10, pady=8, sticky="ew")
            self.entradas[campo] = entrada

        botonFundar = tk.Button(self.ventana, text="Fundar Colonia", command= self.fundar_colonia)
        botonFundar.grid(row=len(self.campos), column=0, columnspan=2, pady=15)

    def fundar_colonia(self):
        datos = {campo: entrada.get().strip() for campo, entrada in self.entradas.items()}
        self.coloniasExistentes[self.key] = Colonia(nombre= datos["Nombre Colonia"])
