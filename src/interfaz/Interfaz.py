import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from pathlib import Path
import threading

from Colono import Colono
from Colonia import Colonia
import Infraestructura
from GestorPersistencia import GestorPersistencia
from interfaz.VentanaColonia import VentanaColonia
from interfaz.VentanaFundar import VentanaFundar
from interfaz.Registro import PanelRegistro
from interfaz import Tema
from eventos.Evento import Evento




class Interfaz:
    def __init__(self):
        self._directorio = Path(__file__).resolve().parent.parent
        self.ventana = tk.Tk()
        Tema.aplicar_tema(self.ventana)  # todas las ventanas en azul oscuro
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
                        infraestructuras= [Infraestructura.Mina(), Infraestructura.Granja(), Infraestructura.Aserradero(), Infraestructura.Huerto()]
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

        for key in self.colonias:
            # Las colonias destruidas por un meteorito no reciben eventos: su planeta esta libre
            if isinstance(self.colonias[key], (Colonia)) and not self.colonias[key].destruida:
                self.colonias[key].iniciar_gestion()
            else:
                pass
        
        # 3. Configurar el autoguardado al pulsar la 'X' para cerrar la ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.al_cerrar_ventana)

        # 4. Crear el Canvas (Lienzo) que ocupa toda la ventana
        self.canvas = tk.Canvas(self.ventana, width=1000, height=1000, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # 5. Cargar elementos visuales (Fondo y Planetas)
        # Fondo
        self.imagenFondo = Image.open(self._directorio/"imagenesPlanetas/fondo.jpeg")
        self.imagenFondo = self.imagenFondo.resize((1000, 1000))
        self.imagenFondo_tk = ImageTk.PhotoImage(self.imagenFondo)
        self.canvas.create_image(0, 0, image=self.imagenFondo_tk, anchor="nw")

        # Planeta A 
        self.imagenPlanetaA = Image.open(self._directorio/"imagenesPlanetas/planetaA.png")
        self.imagenPlanetaA.thumbnail((200, 200))
        self.imagenPlanetaA_tk = ImageTk.PhotoImage(self.imagenPlanetaA)
        self.id_planetaA = self.canvas.create_image(150, 150, image=self.imagenPlanetaA_tk)

        # Planeta B
        self.imagenPlanetaB = Image.open(self._directorio/"imagenesPlanetas/planetaB.png")
        self.imagenPlanetaB.thumbnail((200, 200))
        self.imagenPlanetaB_tk = ImageTk.PhotoImage(self.imagenPlanetaB)
        self.id_planetaB = self.canvas.create_image(400, 350, image=self.imagenPlanetaB_tk)

        # Planeta C
        self.imagenPlanetaC = Image.open(self._directorio/"imagenesPlanetas/planetaC.png")
        self.imagenPlanetaC.thumbnail((200, 200))
        self.imagenPlanetaC_tk = ImageTk.PhotoImage(self.imagenPlanetaC)
        self.id_planetaC = self.canvas.create_image(740, 600, image=self.imagenPlanetaC_tk)

        # 6. Vincular los clics de cada planeta con su respectiva colonia del diccionario
        self.canvas.tag_bind(self.id_planetaA, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["A"], "A"))
        self.canvas.tag_bind(self.id_planetaB, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["B"], "B"))
        self.canvas.tag_bind(self.id_planetaC, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["C"], "C"))

        # 7. Guardar referencias de las imágenes para evitar que el recolector de basura de Python las borre
        self.canvas.image_fondo = self.imagenFondo_tk
        self.canvas.imagePlanetaA = self.imagenPlanetaA_tk
        self.canvas.imagePlanetaB = self.imagenPlanetaB_tk
        self.canvas.imagePlanetaC = self.imagenPlanetaC_tk

        # 8. Registro: lo que se imprime en la terminal tambien se ve aqui, con colores
        self.panelRegistro = PanelRegistro(
            self.ventana,
            nombres_colonias=lambda: [c.nombre for c in self.colonias.values() if isinstance(c, Colonia)],
            titulos_eventos=Evento.Titulos.values(),
        )
        self.registroVisible = False
        self.botonRegistro = tk.Button(self.ventana, text="Registro", command=self.alternar_registro,
                                       bg=Tema.BOTON, fg=Tema.TEXTO, activebackground=Tema.BOTON_ACTIVO,
                                       activeforeground=Tema.TEXTO, relief="flat")
        self.botonRegistro.place(relx=1.0, x=-10, y=10, anchor="ne")
        self.alternar_registro()  # empieza visible

    def alternar_registro(self):
        """Muestra u oculta el panel de registro en la parte de abajo de la ventana."""
        if self.registroVisible:
            self.panelRegistro.place_forget()
            self.botonRegistro.config(text="Mostrar registro")
        else:
            self.panelRegistro.place(relx=0, rely=1.0, x=10, y=-10, relwidth=1.0, width=-20, height=260, anchor="sw")
            self.panelRegistro.lift()
            self.botonRegistro.config(text="Ocultar registro")
        self.registroVisible = not self.registroVisible

    def al_cerrar_ventana(self):
        """Método que se ejecuta automáticamente al cerrar la ventana (guarda antes de salir)."""
        for colonia in self.colonias.values():
            colonia.detener_gestion()
        print("Guardando partida...")
        try:
            self.persistencia.guardar_colonias(self.colonias)
        except Exception as e:
            print(f"Error al guardar la partida: {e}")
        self.ventana.destroy()

    def entrarEnPlaneta(self, evento, colonia: Colonia, key: str):
        """Abre la ventana detallada al hacer clic en un planeta invocando la nueva clase."""
        # Se instancia la ventana pasándole la ventana principal de tkinter como padre y la colonia a mostrar
        if not colonia or colonia.destruida:
            # Planeta libre (nunca colonizado o colonia destruida por un meteorito)
            VentanaFundar(self.ventana, self.colonias, key)
        else:
            VentanaColonia(self.ventana, colonia)
         
    def start(self):
        self.ventana.mainloop()
        for key in self.colonias:
            if isinstance(self.colonias[key], (Colonia)):
                self.colonias[key].detener_gestion()
            else:
                pass
