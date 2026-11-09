import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

from Colono import Colono
from Colonia import Colonia
from GestorPersistencia import GestorPersistencia

class Interfaz:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Colonización de planetas")
        self.ventana.geometry("1000x1000")

        # 1. Inicializar el gestor de persistencia
        self.persistencia = GestorPersistencia()

        # 2. Cargar la partida guardada o crear las colonias iniciales por defecto con objetos Colono
        try:
            self.colonias = self.persistencia.cargar_colonias()
            print("¡Partida cargada con éxito desde el disco!")
        except (FileNotFoundError, ValueError):
            print("No se encontró partida previa. Inicializando colonias por defecto...")
            self.colonias = {
                "A": Colonia(
                    nombre="Kukusclan", 
                    colonos=[Colono("Alfredo", "Kukusclan", 25, 1, "M")], 
                    recursos={"Madera": 20}, 
                    infraestructuras=None
                ),
                "B": Colonia(
                    nombre="La sociedad de la nieve", 
                    colonos=[Colono("Rubén", "La sociedad de la nieve", 30, 1, "M")], 
                    recursos={"Hierro": 30, "Madera": 2}, 
                    infraestructuras=None
                ),
                "C": Colonia(
                    nombre="Sociópatas", 
                    colonos=[Colono("Elena", "Sociópatas" ,22, 1, "F")], 
                    recursos={"Agua": 10}, 
                    infraestructuras=None
                ),
            }

        # 3. Configurar el autoguardado al pulsar la 'X' para cerrar la ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.al_cerrar_ventana)

        # 4. Crear el Canvas (Lienzo) que ocupa toda la ventana
        self.canvas = tk.Canvas(self.ventana, width=1000, height=1000, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # 5. Cargar elementos visuales (Fondo y Planetas)
        # Fondo
        self.imagenFondo = Image.open("imagenesPlanetas/fondo.jpeg")
        self.imagenFondo = self.imagenFondo.resize((1000, 1000))
        self.imagenFondo_tk = ImageTk.PhotoImage(self.imagenFondo)
        self.canvas.create_image(0, 0, image=self.imagenFondo_tk, anchor="nw")

        # Planeta A 
        self.imagenPlanetaA = Image.open("imagenesPlanetas/planetaA.png")
        self.imagenPlanetaA.thumbnail((200, 200))
        self.imagenPlanetaA_tk = ImageTk.PhotoImage(self.imagenPlanetaA)
        self.id_planetaA = self.canvas.create_image(150, 150, image=self.imagenPlanetaA_tk)

        # Planeta B
        self.imagenPlanetaB = Image.open("imagenesPlanetas/planetaB.png")
        self.imagenPlanetaB.thumbnail((200, 200))
        self.imagenPlanetaB_tk = ImageTk.PhotoImage(self.imagenPlanetaB)
        self.id_planetaB = self.canvas.create_image(400, 350, image=self.imagenPlanetaB_tk)

        # Planeta C
        self.imagenPlanetaC = Image.open("imagenesPlanetas/planetaC.png")
        self.imagenPlanetaC.thumbnail((200, 200))
        self.imagenPlanetaC_tk = ImageTk.PhotoImage(self.imagenPlanetaC)
        self.id_planetaC = self.canvas.create_image(740, 600, image=self.imagenPlanetaC_tk)

        # 6. Vincular los clics de cada planeta con su respectiva colonia del diccionario
        self.canvas.tag_bind(self.id_planetaA, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["A"]))
        self.canvas.tag_bind(self.id_planetaB, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["B"]))
        self.canvas.tag_bind(self.id_planetaC, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["C"]))

        # 7. Guardar referencias de las imágenes para evitar que el recolector de basura de Python las borre
        self.canvas.image_fondo = self.imagenFondo_tk
        self.canvas.imagePlanetaA = self.imagenPlanetaA_tk
        self.canvas.imagePlanetaB = self.imagenPlanetaB_tk
        self.canvas.imagePlanetaC = self.imagenPlanetaC_tk

    def al_cerrar_ventana(self):
        """Método que se ejecuta automáticamente al cerrar la ventana (guarda antes de salir)."""
        print("Guardando partida...")
        try:
            self.persistencia.guardar_colonias(self.colonias)
        except Exception as e:
            print(f"Error al guardar la partida: {e}")
        self.ventana.destroy()

    def entrarEnPlaneta(self, evento, colonia: Colonia):
        """Abre la ventana detallada al hacer clic en un planeta."""
        ventanaDetallada = tk.Toplevel(self.ventana)
        ventanaDetallada.title("Estado del planeta")
        ventanaDetallada.geometry("400x400")

        tk.Label(ventanaDetallada, text=f"Nombre de la colonia: {colonia.nombre}", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Label(ventanaDetallada, text=f"Población actual: {colonia.verColonos()}").pack(pady=10)

        tk.Button(ventanaDetallada, text="Cerrar ventana", command=ventanaDetallada.destroy).pack(pady=20)

    def start(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    gui = Interfaz()
    gui.start()