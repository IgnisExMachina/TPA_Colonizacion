import tkinter as tk

from Colonia import Colonia
from Infraestructura import Huerto
from interfaz import Tema


class VentanaHuerto:
    ANCHO = 480
    ALTO_CIELO = 80
    ALTO_FILA = 130
    REFRESCO_MS = 1000  # las plantas crecen desde el hilo de eventos, asi que redibujamos cada segundo

    COLOR_CIELO = "#a8d8ff"
    COLOR_TIERRA = "#7a4b25"
    COLOR_SURCO = "#5c3517"
    COLOR_SEMILLA = "#d9b26f"
    COLOR_PETALO = "#e53935"
    COLOR_CENTRO = "#fdd835"

    def __init__(self, ventana_padre, colonia: Colonia, huerto: Huerto):
        self.colonia = colonia
        self.huerto = huerto
        self._id_refresco = None

        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title(f"Huerto de {colonia.nombre}")
        self.ventana.resizable(False, False) # ? Evitamos que el usuario pueda ajustar la ventana
        self.ventana.configure(bg=Tema.FONDO) # ? Pone tema de la ventana con lo que tenemos en el archivo Tema.py
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar) # ? Destruimos la ventana

        #  ? El canvas es el lienzo donde vamos a dibujar el huerto. Si inviertes en el HUERTO el alto crecerá
        self.canvas = tk.Canvas(self.ventana, width=self.ANCHO, height=self._alto(), highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.etiqueta_info = tk.Label(self.ventana, font=("Arial", 10))
        self.etiqueta_info.pack()

        self.etiqueta_mensaje = tk.Label(self.ventana, font=("Arial", 10, "italic"), fg=Tema.TEXTO_SUAVE)
        self.etiqueta_mensaje.pack(pady=(2, 6))
        # ? El frame crea un "div" donde irán los botones
        botones = tk.Frame(self.ventana)
        botones.pack(pady=(0, 10))
        tk.Button(botones, text="Plantar semilla", command=self.plantar_semilla).pack(side=tk.LEFT, padx=5)
        self.boton_recoger = tk.Button(botones, text="Recoger", command=self.recoger)
        self.boton_recoger.pack(side=tk.LEFT, padx=5)
        tk.Button(botones, text="Cerrar", command=self.cerrar).pack(side=tk.LEFT, padx=5)

        # ! Se pone refrescar() con paréntesis para que se haga la acción insitu
        self.refrescar()

    # TODO: Acciones
    def plantar_semilla(self):
        if self.huerto.parcelas_libres() <= 0:
            self.etiqueta_mensaje.config(text="El huerto está lleno.")
        elif self.colonia.recursos.get("Semillas", 0) < 1:
            self.etiqueta_mensaje.config(text="No quedan semillas. ¡Manda a un colono de exploración!")
        elif self.huerto.plantar(self.colonia):
            self.etiqueta_mensaje.config(text="Semilla plantada.")
        self.dibujar()

    def recoger(self):
        cosecha = self.huerto.recoger(self.colonia)
        if cosecha["Plantas"] == 0:
            self.etiqueta_mensaje.config(text="Todavía no hay nada que recoger.")
        else:
            self.etiqueta_mensaje.config(
                text=f"Has recogido {cosecha['Plantas']} planta(s) y {cosecha['Semillas']} semilla(s)."
            )
        self.dibujar()

    def cerrar(self):
        if self._id_refresco is not None:
            self.ventana.nametowidget(".").after_cancel(self._id_refresco)
            self._id_refresco = None
        self.ventana.destroy()

    # TODO: Dibujo
    def _columnas(self) -> int:
        # Invertir en el huerto da mas parcelas: se reparten en mas columnas y filas
        n = self.huerto.num_parcelas()
        return 3 if n <= 6 else 4 if n <= 8 else 5

    def _filas(self) -> int:
        return -(-self.huerto.num_parcelas() // self._columnas())  # division redondeando hacia arriba

    def _alto(self) -> int:
        return self.ALTO_CIELO + self._filas() * self.ALTO_FILA
    def refrescar(self):
        # ? Si la ventana se ha cerrado (por ejemplo al cerrar la del planeta) dejamos de refrescar
        if not self.ventana.winfo_exists():
            self._id_refresco = None
            return
        self.dibujar()
        # ? Se programa en la ventana principal para que no falle si esta ventana se destruye
        self._id_refresco = self.ventana.nametowidget(".").after(self.REFRESCO_MS, self.refrescar)

    def dibujar(self):
        c = self.canvas
        c.delete("all")

        # ? Si se ha invertido en el huerto mientras estaba abierto, el lienzo crece
        alto = self._alto()
        if int(c.cget("height")) != alto:
            c.config(height=alto)
        columnas = self._columnas()

        # ? Cielo y tierra
        horizonte = self.ALTO_CIELO
        c.create_rectangle(0, 0, self.ANCHO, horizonte, fill=self.COLOR_CIELO, outline="")
        c.create_rectangle(0, horizonte, self.ANCHO, alto, fill=self.COLOR_TIERRA, outline="")

        # ? Parcelas (surcos)
        ancho_celda = self.ANCHO / columnas
        alto_celda = self.ALTO_FILA
        ancho_surco = min(55, ancho_celda / 2 - 8)
        plantas = list(self.huerto.plantas)  # copia: el hilo de eventos puede modificarla

        # ? Calcula dónde va cada parcela en el canvas. Se saca el punto central donde se dibuja su surco (y encima la semilla/flor).
        for i in range(self.huerto.num_parcelas()):
            fila, col = divmod(i, columnas) # ! divmod hace la división entera y el resto a la vez
            cx = col * ancho_celda + ancho_celda / 2
            cy = horizonte + fila * alto_celda + alto_celda * 0.7

            c.create_oval(cx - ancho_surco, cy - 12, cx + ancho_surco, cy + 12, fill=self.COLOR_SURCO, outline="")

            if i < len(plantas):
                self._dibujar_planta(cx, cy, plantas[i])

        # ? Nos da info dentro de la ventana sobre semilas, plantas, parcelas
        maduras = self.huerto.plantas_maduras()
        self.etiqueta_info.config(
            text=(f"Semillas: {self.colonia.recursos.get('Semillas', 0)}   |   "
                  f"Plantas en inventario: {self.colonia.recursos.get('Plantas', 0)}   |   "
                  f"Parcelas libres: {self.huerto.parcelas_libres()}/{self.huerto.num_parcelas()}   |   "
                  f"Listas: {maduras}")
        )
        self.boton_recoger.config(state=tk.NORMAL if maduras else tk.DISABLED)

    
    def _dibujar_planta(self, x, y, eventos_crecidos):
        c = self.canvas
        total = self.huerto.EVENTOS_PARA_CRECER

        if eventos_crecidos < total:
            # Semilla: se queda asi hasta que la planta este lista
            c.create_oval(x - 6, y - 5, x + 6, y + 3, fill=self.COLOR_SEMILLA, outline="#8d6e3f")
        else:
            # Flor lista para recoger: cuatro petalos y un centro
            cy = y - 15
            for dx, dy in ((0, -10), (10, 0), (0, 10), (-10, 0)):
                c.create_oval(x + dx - 8, cy + dy - 8, x + dx + 8, cy + dy + 8, fill=self.COLOR_PETALO, outline="")
            c.create_oval(x - 6, cy - 6, x + 6, cy + 6, fill=self.COLOR_CENTRO, outline="")

        # ? Nos dice el número de eventos que han sucedido y los que quedan (2/5)
        c.create_text(x, y + 22, text=f"{min(eventos_crecidos, total)}/{total}", fill="white", font=("Arial", 9))
