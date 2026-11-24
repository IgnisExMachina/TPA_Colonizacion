"""Registro de lo que pasa en la partida dentro de la interfaz.

- RedirectorSalida: sustituye a sys.stdout. Todo lo que el juego imprime con print se sigue mostrando
  en la terminal y ademas se mete en una cola. Los errores (stderr) solo salen en la terminal.
- PanelRegistro: panel de Tkinter que lee esa cola y pinta cada linea con un color segun lo que dice.

Los eventos se imprimen desde los hilos de las colonias y Tkinter no se puede tocar desde otro hilo,
por eso los hilos solo meten texto en la cola y es el panel (en el hilo de la interfaz) quien la lee.
"""
import queue
import sys
import threading
import tkinter as tk
from datetime import datetime

from interfaz import Tema

# Cola compartida entre los redirectores y el panel: (texto, es_error)
_cola_lineas: queue.Queue = queue.Queue()


class RedirectorSalida:
    def __init__(self, salida_original, es_error: bool = False):
        self._original = salida_original
        self._es_error = es_error
        # Cada hilo tiene su propio buffer para que no se mezclen trozos de lineas de distintas colonias
        self._local = threading.local()

    def write(self, texto: str):
        if self._original is not None:
            self._original.write(texto)
        buffer = getattr(self._local, "buffer", "") + texto
        *lineas, resto = buffer.split("\n")
        self._local.buffer = resto
        for linea in lineas:
            _cola_lineas.put((linea, self._es_error))
        return len(texto)

    def flush(self):
        if self._original is not None:
            self._original.flush()

    def __getattr__(self, nombre):
        # encoding, isatty, fileno... se delegan en la salida original
        return getattr(self._original, nombre)


def instalar_redireccion():
    """Solo se redirige stdout (los print del juego). Los errores, tracebacks y mensajes de logging
    van a stderr y se quedan unicamente en la terminal: no se muestran en el registro de la app."""
    if not isinstance(sys.stdout, RedirectorSalida):
        sys.stdout = RedirectorSalida(sys.stdout)


class PanelRegistro(tk.Frame):
    MAX_LINEAS = 200
    REFRESCO_MS = 200

    FONDO = Tema.PANEL
    COLOR_HORA = Tema.TEXTO_APAGADO

    # (etiqueta, color, palabras clave). Se comprueban en este orden y gana la primera que coincide.
    CATEGORIAS = [
        ("peligro", "#ff6b6b", ["muere", "meteorito", "destruida", "afecta a la infraestructura",
                                "error", "inoperativa", "traceback", "exception", "[warning]"]),
        ("aviso", "#ffb74d", ["consumido", "no hay", "lleno", "no tiene", "ocupado", "no puede"]),
        ("bueno", "#81c784", ["se unen", "vuelve de explorar", "cosecha", "con éxito", "plantado",
                              "reparada", "colonizado", "cargad", "guardad"]),
        ("exploracion", "#64b5f6", ["sale de exploración", "crecen", "iniciada en paralelo"]),
        ("produccion", "#b0b0b0", ["produce", "extraíd", "extraer", "producido", "aumenta",
                                   "añadido", "recursos utilizados", "\t-"]),
        ("info", Tema.TEXTO_SUAVE, ["[info]"]),
    ]
    COLOR_EVENTO = "#ffb74d"   # lineas tipo "Tormenta!" con el titulo de un evento
    COLOR_COLONIA = "#90caf9"  # cabecera con el nombre de la colonia antes de cada evento
    COLOR_NORMAL = Tema.TEXTO

    def __init__(self, padre, nombres_colonias=None, titulos_eventos=None):
        """nombres_colonias: funcion que devuelve los nombres actuales de las colonias.
        titulos_eventos: titulos de los eventos (Llovizna, Asedio...) para colorearlos."""
        super().__init__(padre, bg=self.FONDO, highlightbackground=Tema.BORDE, highlightthickness=2)
        self._nombres_colonias = nombres_colonias or (lambda: [])
        self._titulos_eventos = {t.lower() for t in (titulos_eventos or [])}

        cabecera = tk.Frame(self, bg=Tema.CABECERA)
        cabecera.pack(fill=tk.X)
        tk.Label(cabecera, text="Registro de la galaxia", bg=Tema.CABECERA, fg=Tema.TEXTO,
                 font=("Arial", 10, "bold"), padx=10, pady=4).pack(side=tk.LEFT)
        tk.Button(cabecera, text="Limpiar", command=self.limpiar, bg=Tema.CABECERA, fg=Tema.TEXTO,
                  relief="flat", activebackground=Tema.BOTON_ACTIVO).pack(side=tk.RIGHT, padx=4)

        self._scroll = tk.Scrollbar(self)
        self._scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto = tk.Text(self, bg=self.FONDO, fg=self.COLOR_NORMAL, font=("Courier", 10),
                             wrap="word", relief="flat", padx=8, pady=6, state=tk.DISABLED,
                             yscrollcommand=self._scroll.set, insertbackground=self.FONDO)
        self.texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._scroll.config(command=self.texto.yview)

        self.texto.tag_configure("hora", foreground=self.COLOR_HORA)
        self.texto.tag_configure("normal", foreground=self.COLOR_NORMAL)
        self.texto.tag_configure("evento", foreground=self.COLOR_EVENTO, font=("Courier", 10, "bold"))
        self.texto.tag_configure("colonia", foreground=self.COLOR_COLONIA, font=("Courier", 10, "bold"))
        for etiqueta, color, _ in self.CATEGORIAS:
            self.texto.tag_configure(etiqueta, foreground=color)

        self._leer_cola()

    def _clasificar(self, linea: str, es_error: bool) -> str:
        limpia = linea.strip()
        if es_error and "[info]" not in limpia.lower():
            return "peligro"
        if limpia in self._nombres_colonias():
            return "colonia"
        minus = linea.lower()
        # Primero lo peligroso (asi "Asedio! Juan muere en combate" sale en rojo y no como evento)
        etiqueta, _, claves = self.CATEGORIAS[0]
        if any(clave in minus for clave in claves):
            return etiqueta
        if minus.split("!")[0].strip() in self._titulos_eventos:
            return "evento"
        for etiqueta, _, claves in self.CATEGORIAS[1:]:
            if any(clave in minus for clave in claves):
                return etiqueta
        return "normal"

    def escribir(self, linea: str, es_error: bool = False):
        if not linea.strip():
            return
        etiqueta = self._clasificar(linea, es_error)
        if etiqueta == "colonia":
            linea = f"── {linea.strip()} ──"

        # Solo bajamos solos si el usuario ya estaba abajo del todo (si esta leyendo arriba, no le movemos)
        estaba_abajo = self.texto.yview()[1] >= 0.999
        self.texto.config(state=tk.NORMAL)
        self.texto.insert(tk.END, datetime.now().strftime("%H:%M:%S "), "hora")
        self.texto.insert(tk.END, linea.replace("\t", "    ") + "\n", etiqueta)
        sobran = int(self.texto.index("end-1c").split(".")[0]) - 1 - self.MAX_LINEAS
        if sobran > 0:
            self.texto.delete("1.0", f"{sobran + 1}.0")
        self.texto.config(state=tk.DISABLED)
        if estaba_abajo:
            self.texto.see(tk.END)

    def limpiar(self):
        self.texto.config(state=tk.NORMAL)
        self.texto.delete("1.0", tk.END)
        self.texto.config(state=tk.DISABLED)

    def _leer_cola(self):
        if not self.winfo_exists():
            return
        try:
            while True:
                linea, es_error = _cola_lineas.get_nowait()
                self.escribir(linea, es_error)
        except queue.Empty:
            pass
        self.after(self.REFRESCO_MS, self._leer_cola)
