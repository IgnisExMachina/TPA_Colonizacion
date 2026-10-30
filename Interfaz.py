import tkinter as tk
from PIL import Image, ImageTk # ! Instalar en la terminal, en el directorio del proyecto pip install Pillow
import random

from Colonia import Colonia

class Interfaz:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Colonización de planetas")
        self.ventana.geometry("1000x1000")


        # ! 1. Crear el Canvas (Lienzo) que ocupará TODA la ventana
        self.canvas = tk.Canvas(self.ventana, width=1000, height=1000, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)


        # ? CREAR MAPA CON TODOS LOS PLANETAS

        # ? FONDO
        self.imagenFondo = Image.open("imagenesPlanetas/fondo.jpeg")
        self.imagenFondo = self.imagenFondo.resize((1000, 1000))
        self.imagenFondo_tk = ImageTk.PhotoImage(self.imagenFondo)
        # "nw" es que se coloca desde la esquina NorOeste (arriba a la izquierda)
        self.canvas.create_image(0, 0, image=self.imagenFondo_tk, anchor="nw")

        # ? PLANETA A 
        self.imagenPlanetaA = Image.open("imagenesPlanetas/planetaA.png")
        self.imagenPlanetaA.thumbnail((200, 200))
        self.imagenPlanetaA_tk = ImageTk.PhotoImage(self.imagenPlanetaA)
        self.id_planetaA = self.canvas.create_image(150, 150, image=self.imagenPlanetaA_tk)

        # ? PLANETA B
        self.imagenPlanetaB = Image.open("imagenesPlanetas/planetaB.png")
        self.imagenPlanetaB.thumbnail((200, 200)) #! NO PONEMOS imagenPlanetaB = imagenPlanetaB.thumbnail((200, 200)) porque pega error
        self.imagenPlanetaB_tk = ImageTk.PhotoImage(self.imagenPlanetaB)
        self.id_planetaB = self.canvas.create_image(400, 350, image=self.imagenPlanetaB_tk)

        # ? PLANETA C
        self.imagenPlanetaC = Image.open("imagenesPlanetas/planetaC.png")
        self.imagenPlanetaC.thumbnail((200, 200))
        self.imagenPlanetaC_tk = ImageTk.PhotoImage(self.imagenPlanetaC)
        self.id_planetaC = self.canvas.create_image(740, 600, image=self.imagenPlanetaC_tk)

                # 2. Vinculas el clic usando lambda para pasarle el objeto correspondiente a cada dibujo
        self.canvas.tag_bind(self.id_planetaA, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, colonia_A))
        self.canvas.tag_bind(self.id_planetaB, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, colonia_B))
        self.canvas.tag_bind(self.id_planetaC, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, colonia_C))


        # 5. IMPORTANTE: Guardar referencias para que el recolector de basura no las borre
        self.canvas.image_fondo = self.imagenFondo_tk
        self.canvas.imagePlanetaA = self.imagenPlanetaA_tk
        self.canvas.imagePlanetaB = self.imagenPlanetaB_tk
        self.canvas.imagePlanetaC = self.imagenPlanetaC_tk



    def entrarEnPlaneta(self, evento, colonia: Colonia) :
        self.ventanaDetallada = tk.Toplevel()
        self.ventanaDetallada.title("Estado del planeta")
        self.ventanaDetallada.geometry("400x400")

        tk.Label(self.ventanaDetallada, text=f"Nombre de la colonia: {colonia.nombre}").pack(pady=10)
        tk.Label(self.ventanaDetallada, text= f"Población actual: {colonia.verColonos()}").pack(pady=10)

        tk.Button(self.ventanaDetallada, text="Cerrar ventana", command = self.ventanaDetallada.destroy).pack(pady=20)
    
    def start(self):
        self.ventana.mainloop()

# TODO: EVENTOS
# ? Ahora creamos el evento de click





# TODO: PRUEBAS --------------------------------------
colonia_A = Colonia("Kukusclan", ["Alfredo", "Rubén", "Elena"], ["Madera", "Hierro"], None)
colonia_B = Colonia("La sociedad de la nieve", ["Alfredo", "Rubén", "Elena"], ["Madera", "Hierro"], None)
colonia_C = Colonia("Sociópatas", ["Alfredo", "Rubén", "Elena"], ["Madera", "Hierro"], None)

colonia_A.verColonos()
 

GUI = Interfaz()
GUI.start()


