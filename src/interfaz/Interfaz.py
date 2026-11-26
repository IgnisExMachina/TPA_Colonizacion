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
        coloniasVaciasPorDefecto = []
        for i in range(3):
            coloniasVaciasPorDefecto.append(Colonia())
            coloniasVaciasPorDefecto[i].noFundada = True
        self._directorio = Path(__file__).resolve().parent.parent
        self.ventana = tk.Tk()
        Tema.aplicar_tema(self.ventana)  # todas las ventanas en azul oscuro
        self.ventana.title("Colonización de planetas")
        # Tamaño inicial segun la pantalla: como mucho 1000x1000, pero que quepa en portatiles pequeños
        lado = int(min(1000, self.ventana.winfo_screenwidth() * 0.9, self.ventana.winfo_screenheight() * 0.85))
        x = (self.ventana.winfo_screenwidth() - lado) // 2
        y = max(0, (self.ventana.winfo_screenheight() - lado) // 2 - 30)
        self.ventana.geometry(f"{lado}x{lado}+{x}+{y}")
        self.ventana.minsize(500, 500)

        # 1. Inicializar el gestor de persistencia
        self.persistencia = GestorPersistencia()

        # 2. Cargar la partida guardada o crear las colonias iniciales por defecto con objetos Colono
        try:
            self.colonias = self.persistencia.cargar_colonias()
            print("¡Partida cargada con éxito desde el disco!")
        except (FileNotFoundError, ValueError):
            print("No se encontró partida previa. Inicializando colonias por defecto...")
            self.colonias = {
<<<<<<< HEAD
                "A": Colonia(
                        nombre="Kukusclan", 
                        colonos=[Colono("Alfredo", "Kukusclan", 25, 1, "M")], 
                        recursos={"Madera": 20}, 
                        infraestructuras= []
                    ),
                "B": Colonia(
                        nombre="La sociedad de la nieve", 
                        colonos=[Colono("Rubén", "La sociedad de la nieve", 30, 1, "M")], 
                        recursos={"Hierro": 30, "Madera": 20}, 
                        infraestructuras=None
                    ),
                "C": Colonia(
                        nombre="Sociópatas", 
                        colonos=[Colono("Elena", "Sociópatas" ,22, 1, "F")], 
                        recursos={"Agua": 10}, 
                        infraestructuras=None
                    ),
=======
                "A": coloniasVaciasPorDefecto[0],
                "B": coloniasVaciasPorDefecto[1],
                "C": coloniasVaciasPorDefecto[2],
>>>>>>> 0255c801067af07317fa1a43c541eebfd1a934ca
                }

        for key in self.colonias:
            # Las colonias destruidas por un meteorito no reciben eventos: su planeta esta libre
            if isinstance(self.colonias[key], (Colonia)) and not self.colonias[key].destruida and not self.colonias[key].nombre == "-":
                self.colonias[key].iniciar_gestion()
            else:
                pass
        
        # 3. Configurar el autoguardado al pulsar la 'X' para cerrar la ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.al_cerrar_ventana)

        # 4. Crear el Canvas (Lienzo) que ocupa toda la ventana
        self.canvas = tk.Canvas(self.ventana, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # 5. Cargar elementos visuales (Fondo y Planetas)
        # Guardamos las imagenes originales sin redimensionar: cada vez que cambia el tamaño
        # de la ventana se reescalan a partir de ellas (si no, perderian calidad)
        carpeta = self._directorio/"imagenesPlanetas"
        self.imagenFondo = Image.open(carpeta/"fondo.jpeg")
        self.id_fondo = self.canvas.create_image(0, 0, anchor="nw")

        # Cada planeta: (imagen original, id en el canvas, posicion relativa x, posicion relativa y)
        # Las posiciones van de 0 a 1 respecto al ancho y alto de la ventana
        self.planetas = {}
        for key, archivo, rx, ry in (("A", "planetaD.png", 0.15, 0.15),
                                     ("B", "planetaB.png", 0.40, 0.35),
                                     ("C", "planetaC.png", 0.74, 0.60)):
            id_planeta = self.canvas.create_image(0, 0)
            self.planetas[key] = (Image.open(carpeta/archivo), id_planeta, rx, ry)
        self.id_planetaA = self.planetas["A"][1]
        self.id_planetaB = self.planetas["B"][1]
        self.id_planetaC = self.planetas["C"][1]

        # Referencias a las imagenes de tkinter para que el recolector de basura de Python no las borre
        self._imagenes_tk = {}
        self._id_reescalado = None
        self._tamano_dibujado = None
        self.canvas.bind("<Configure>", self._programar_reescalado)

        # 6. Vincular los clics de cada planeta con su respectiva colonia del diccionario
        self.canvas.tag_bind(self.id_planetaA, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["A"], "A"))
        self.canvas.tag_bind(self.id_planetaB, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["B"], "B"))
        self.canvas.tag_bind(self.id_planetaC, "<Button-1>", lambda evento: self.entrarEnPlaneta(evento, self.colonias["C"], "C"))

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
            # La altura es relativa (28% de la ventana) para que en pantallas pequeñas no lo tape todo
            self.panelRegistro.place(relx=0, rely=1.0, x=10, y=-10, relwidth=1.0, width=-20, relheight=0.28, anchor="sw")
            self.panelRegistro.lift()
            self.botonRegistro.config(text="Ocultar registro")
        self.registroVisible = not self.registroVisible

    def _programar_reescalado(self, evento):
        """Al arrastrar el borde de la ventana llegan muchos eventos seguidos: esperamos un poco
        y solo reescalamos con el ultimo, para que no vaya a tirones."""
        if self._id_reescalado is not None:
            self.ventana.after_cancel(self._id_reescalado)
        self._id_reescalado = self.ventana.after(60, self._reescalar)

    def _reescalar(self):
        """Ajusta el fondo y los planetas al tamaño actual del canvas."""
        self._id_reescalado = None
        ancho, alto = self.canvas.winfo_width(), self.canvas.winfo_height()
        if ancho < 2 or alto < 2 or (ancho, alto) == self._tamano_dibujado:
            return
        self._tamano_dibujado = (ancho, alto)

        # El fondo ocupa todo el canvas
        self._imagenes_tk["fondo"] = ImageTk.PhotoImage(self.imagenFondo.resize((ancho, alto)))
        self.canvas.itemconfig(self.id_fondo, image=self._imagenes_tk["fondo"])

        # Los planetas miden un 20% del lado mas corto y se colocan en su posicion relativa.
        # Se reutilizan los mismos ids, asi que los clics (tag_bind) siguen funcionando
        lado = max(1, int(min(ancho, alto) * 0.2))
        for key, (original, id_planeta, rx, ry) in self.planetas.items():
            imagen = original.copy()
            imagen.thumbnail((lado, lado))
            self._imagenes_tk[key] = ImageTk.PhotoImage(imagen)
            self.canvas.itemconfig(id_planeta, image=self._imagenes_tk[key])
            self.canvas.coords(id_planeta, rx * ancho, ry * alto)

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
        if not colonia or colonia.destruida or colonia.abandonada or colonia.noFundada:
            # Planeta libre (nunca colonizado o colonia destruida por un meteorito)
             VentanaFundar(self.ventana, self.colonias, key)
        else:
            VentanaColonia(self.ventana, colonia, self.colonias)
         
    def start(self):
        self.ventana.mainloop()
        for key in self.colonias:
            if isinstance(self.colonias[key], (Colonia)):
                self.colonias[key].detener_gestion()
            else:
                pass
