import tkinter as tk
from PIL import Image, ImageTk # ! Instalar en la terminal, en el directorio del proyecto pip install Pillow
import random

from Colonia import Colonia

# TODO: EVENTOS
# ? Ahora creamos el evento de click
def entrarEnPlaneta(evento, colonia: Colonia) :
    ventanaDetallada = tk.Toplevel()
    ventanaDetallada.title("Estado del planeta")
    ventanaDetallada.geometry("400x400")

    poblacion = random.randint(0, 30)
    minerales = random.randint(0, 1000)

    tk.Label(ventanaDetallada, text=f"Nombre de la colonia: {colonia.nombre}").pack(pady=10)
    tk.Label(ventanaDetallada, text= f"Población actual: {colonia.verColonos()}").pack(pady=10)

    tk.Button(ventanaDetallada, text="Cerrar ventana", command = ventanaDetallada.destroy).pack(pady=20)



ventana = tk.Tk()
ventana.title("Colonización de planetas")
ventana.geometry("1000x1000")


# ! 1. Crear el Canvas (Lienzo) que ocupará TODA la ventana
canvas = tk.Canvas(ventana, width=1000, height=1000, highlightthickness=0)
canvas.pack(fill="both", expand=True)


# ? CREAR MAPA CON TODOS LOS PLANETAS

# ? FONDO
rutaFondo = "imagenesPlanetas/fondo.jpeg"
imagenFondo = Image.open(rutaFondo)
imagenFondo = imagenFondo.resize((1000, 1000))
imagenFondo_tk = ImageTk.PhotoImage(imagenFondo)
# "nw" es que se coloca desde la esquina NorOeste (arriba a la izquierda)
canvas.create_image(0, 0, image=imagenFondo_tk, anchor="nw")

# ? PLANETA A 
imagenPlanetaA = Image.open("imagenesPlanetas/planetaA.png")
imagenPlanetaA.thumbnail((200, 200))
imagenPlanetaA_tk = ImageTk.PhotoImage(imagenPlanetaA)
id_planetaA = canvas.create_image(150, 150, image=imagenPlanetaA_tk)

# ? PLANETA B
rutaPlanetaB = "imagenesPlanetas/planetaB.png"
imagenPlanetaB = Image.open(rutaPlanetaB)
imagenPlanetaB.thumbnail((200, 200)) #! NO PONEMOS imagenPlanetaB = imagenPlanetaB.thumbnail((200, 200)) porque pega error
imagenPlanetaB_tk = ImageTk.PhotoImage(imagenPlanetaB)
id_planetaB = canvas.create_image(400, 350, image=imagenPlanetaB_tk)

# ? PLANETA C
rutaPlanetaC = "imagenesPlanetas/planetaC.png"
imagenPlanetaC = Image.open(rutaPlanetaC)
imagenPlanetaC.thumbnail((200, 200))
imagenPlanetaC_tk = ImageTk.PhotoImage(imagenPlanetaC)
id_planetaC = canvas.create_image(740, 600, image=imagenPlanetaC_tk)


# En Canvas se usa tag_bind en lugar de bind, apuntando a la ID 
canvas.tag_bind(id_planetaA, "<Button-1>", entrarEnPlaneta)
canvas.tag_bind(id_planetaB, "<Button-1>", entrarEnPlaneta)
canvas.tag_bind(id_planetaC, "<Button-1>", entrarEnPlaneta)

# TODO: PRUEBAS --------------------------------------
colonia_A = Colonia("Kukusclan", ["Alfredo", "Rubén", "Elena"], ["Madera", "Hierro"], None)
colonia_B = Colonia("La sociedad de la nieve", ["Alfredo", "Rubén", "Elena"], ["Madera", "Hierro"], None)
colonia_C = Colonia("Sociópatas", ["Alfredo", "Rubén", "Elena"], ["Madera", "Hierro"], None)

colonia_A.verColonos()
 
# 2. Vinculas el clic usando lambda para pasarle el objeto correspondiente a cada dibujo
canvas.tag_bind(id_planetaA, "<Button-1>", lambda evento: entrarEnPlaneta(evento, colonia_A))
canvas.tag_bind(id_planetaB, "<Button-1>", lambda evento: entrarEnPlaneta(evento, colonia_B))
canvas.tag_bind(id_planetaC, "<Button-1>", lambda evento: entrarEnPlaneta(evento, colonia_C))


# 5. IMPORTANTE: Guardar referencias para que el recolector de basura no las borre
canvas.image_fondo = imagenFondo_tk
canvas.imagePlanetaA = imagenPlanetaA_tk
canvas.imagePlanetaB = imagenPlanetaB_tk
canvas.imagePlanetaC = imagenPlanetaC_tk



ventana.mainloop()

