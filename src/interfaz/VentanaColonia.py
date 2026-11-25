import tkinter as tk
from Colonia import Colonia
import Infraestructura
from interfaz.VentanaHuerto import VentanaHuerto
from interfaz.VentanaNave import VentanaNave
from interfaz import Tema


#TODO: al seleccionar nave espacial existente, se busca un planeta vacio (una colonia que no esté presente)
#! AÑADIR OPCIONES DE FUNDAR COLONIA

class VentanaColonia:
     REFRESCO_MS = 1000  # los menus se actualizan solos (exploraciones, eficiencias...)
     ALTO_MAX_MENU = 350 # a partir de esta altura (en pixeles) el menu tiene barra de scroll

     def __init__(self, ventana_padre, colonia: Colonia, colonias: dict):
          self.colonia = colonia
          self.colonias = colonias #? VentanaNave necesita todas las colonias
          self.estoyEnLaVentana = None
          self._es_menu = False      # True si la subventana es un menu de clic (no se cierra al quitar el raton)
          self._menu = None          # (firma, construir) del menu abierto
          self._firma_menu = None
          self._id_refresco = None
          self._pos_subventana = (0, 0)
        
          # Creamos la ventana hija
          self.ventana = tk.Toplevel(ventana_padre)
          self.ventana.title("Estado del planeta")
          self.ventana.geometry("400x420")
          self.ventana.configure(bg=Tema.FONDO)
          if not colonia:
               #NUNCA deberia darse. lo dejo por si acaso
               tk.Label(self.ventana, text="Planeta no ocupado.", font=("Arial", 11, "bold")).pack(pady=10)
          else:
               tk.Label(self.ventana, text=f"Nombre de la colonia: {self.colonia.nombre}", font=("Arial", 11, "bold")).pack(pady=10)
          
               botonVerColonos = tk.Button(self.ventana, text="Ver población actual")
               botonVerColonos.pack(pady=10)
               # Menu de clic: desde aqui se envia a los colonos de exploracion
               botonVerColonos.bind("<Button-1>", self.abrir_menu_colonos)

               botonVerRecursos = tk.Button(self.ventana, text= "Ver recursos")
               botonVerRecursos.pack(pady=10)

               botonVerRecursos.bind("<Enter>", self.mostrarRecursos)
               botonVerRecursos.bind("<Leave>", self.ocultar_subventana)

               botonVerInfraestructuras = tk.Button (self.ventana, text = "Ver infraestructuras")
               botonVerInfraestructuras.pack(pady=10)
               # Menu de clic: desde aqui se abre el huerto
               botonVerInfraestructuras.bind("<Button-1>", self.abrir_menu_infraestructuras)

               botonMenuInfraestructuras = tk.Button(self.ventana, text = "Menú de construcción")
               botonMenuInfraestructuras.pack(pady=10)

               botonMenuInfraestructuras.bind("<Button-1>", self.abrir_menu_construccion)
               #Mostrar las infraestructuras y sus costes. si se pueden construir, poder hacerlo.

               #tk.Label(self.ventana, text=f"Evento actual: {next(self.colonia._stream)}").pack(pady=10)
               tk.Button(self.ventana, text="Cerrar ventana", command=self.ventana.destroy).pack(pady=20)

     # ---------- Subventanas (tooltips y menus) ----------
     def mostrar_subventana(self, evento) -> bool:
          """Crea la subventana junto al raton. Devuelve False si ya habia una abierta."""
          if self.estoyEnLaVentana is not None and self.estoyEnLaVentana.winfo_exists():
               return False
          self.estoyEnLaVentana = tk.Toplevel(self.ventana)
          self.estoyEnLaVentana.wm_overrideredirect(True)
          
          self._pos_subventana = (evento.x_root + 15, evento.y_root + 15)
          self.estoyEnLaVentana.geometry(f"+{self._pos_subventana[0]}+{self._pos_subventana[1]}")
          return True

     def _ajustar_posicion_subventana(self):
          """Mueve la subventana para que no se salga de la pantalla."""
          sub = self.estoyEnLaVentana
          if sub is None or not sub.winfo_exists():
               return
          sub.update_idletasks()
          ancho, alto = sub.winfo_reqwidth(), sub.winfo_reqheight()
          x, y = self._pos_subventana
          x = max(0, min(x, sub.winfo_screenwidth() - ancho - 10))
          y = max(0, min(y, sub.winfo_screenheight() - alto - 50))
          sub.geometry(f"+{x}+{y}")

     def ocultar_subventana(self, evento):
          # Al quitar el raton solo se cierran los tooltips, los menus se cierran con su boton
          if self._es_menu:
               return
          self.cerrar_subventana()

     def cerrar_subventana(self):
          if self._id_refresco is not None:
               self._raiz().after_cancel(self._id_refresco)
               self._id_refresco = None
          if self.estoyEnLaVentana is not None:
               self.estoyEnLaVentana.destroy()
               self.estoyEnLaVentana = None
          self._es_menu = False
          self._menu = None

     def _raiz(self):
          # Los refrescos se programan en la ventana principal para que no fallen si se cierra esta
          return self.ventana.nametowidget(".")

     def _abrir_menu(self, evento, firma, construir):
          """Abre un menu de clic con el estilo del menu de construccion.
          firma(): devuelve algo que cambia cuando hay que redibujar el menu.
          construir(contenedor): crea los botones del menu."""
          self.cerrar_subventana()
          self.mostrar_subventana(evento)
          self._es_menu = True
          self._menu = (firma, construir)
          self._firma_menu = object()  # fuerza el primer dibujado
          self._crear_esqueleto_menu()
          self._refrescar_menu()

     def _crear_esqueleto_menu(self):
          """Boton de cerrar fijo abajo y, encima, una zona con scroll donde van los botones del menu."""
          sub = self.estoyEnLaVentana
          tk.Button(sub, text="Cerrar ventana", command=self.cerrar_subventana).pack(side=tk.BOTTOM, pady=5)

          zona = tk.Frame(sub)
          zona.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
          self._scroll = tk.Scrollbar(zona, orient=tk.VERTICAL)
          self._lienzo_menu = tk.Canvas(zona, highlightthickness=0, yscrollcommand=self._scroll.set)
          self._scroll.config(command=self._lienzo_menu.yview)
          self._lienzo_menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

          self._contenido_menu = tk.Frame(self._lienzo_menu)
          self._lienzo_menu.create_window(0, 0, window=self._contenido_menu, anchor="nw")

          # Rueda del raton (Windows/Mac: MouseWheel, Linux: Button-4/5)
          sub.bind("<MouseWheel>", lambda e: self._lienzo_menu.yview_scroll(-1 if e.delta > 0 else 1, "units"))
          sub.bind("<Button-4>", lambda e: self._lienzo_menu.yview_scroll(-1, "units"))
          sub.bind("<Button-5>", lambda e: self._lienzo_menu.yview_scroll(1, "units"))

     def _ajustar_tamano_menu(self):
          """El menu ocupa lo que necesite, pero como mucho ALTO_MAX_MENU; si no cabe, aparece la barra de scroll."""
          self._contenido_menu.update_idletasks()
          ancho = self._contenido_menu.winfo_reqwidth()
          alto = self._contenido_menu.winfo_reqheight()
          alto_max = min(self.ALTO_MAX_MENU, int(self.estoyEnLaVentana.winfo_screenheight() * 0.6))
          self._lienzo_menu.config(width=ancho, height=min(alto, alto_max), scrollregion=(0, 0, ancho, alto))
          if alto > alto_max:
               self._scroll.pack(side=tk.RIGHT, fill=tk.Y)
          else:
               self._scroll.pack_forget()

     def _refrescar_menu(self):
          self._id_refresco = None
          if not self._es_menu or self.estoyEnLaVentana is None or not self.estoyEnLaVentana.winfo_exists():
               return
          firma, construir = self._menu
          nueva_firma = firma()
          if nueva_firma != self._firma_menu:
               primera_vez = not self._contenido_menu.winfo_children()
               self._firma_menu = nueva_firma
               posicion_scroll = self._lienzo_menu.yview()[0]  # para no volver arriba en cada refresco
               for hijo in self._contenido_menu.winfo_children():
                    hijo.destroy()
               construir(self._contenido_menu)
               self._ajustar_tamano_menu()
               self._lienzo_menu.yview_moveto(posicion_scroll)
               if primera_vez:
                    self._ajustar_posicion_subventana()
          self._id_refresco = self._raiz().after(self.REFRESCO_MS, self._refrescar_menu)

     def _boton_menu(self, contenedor, texto, comando=None):
          btn = tk.Button(
               contenedor,
               text=texto,
               bg=Tema.PANEL,
               fg=Tema.TEXTO,
               relief="flat",
               anchor="w",
               command=comando,
          )
          if comando is None:
               btn.config(state=tk.DISABLED, disabledforeground=Tema.TEXTO_SUAVE)
          btn.pack(fill=tk.X, expand=True, pady=1)
          return btn

     # ---------- Poblacion ----------
     def abrir_menu_colonos(self, evento):
          self._abrir_menu(evento, self._firma_colonos, self._construir_menu_colonos)

     def _firma_colonos(self):
          return tuple((id(c), c.ocupado, getattr(c, "exploracion_restante", 0)) for c in self.colonia.colonos)

     def _construir_menu_colonos(self, contenedor):
          if not self.colonia.colonos:
               self._boton_menu(contenedor, "No hay colonos registrados.")
               return
          tk.Label(contenedor, text="Pulsa un colono para enviarlo de exploración", font=("Arial", 9, "italic"), fg=Tema.TEXTO_SUAVE).pack(fill=tk.X)
          for colono in self.colonia.colonos:
               texto = f"{colono.nombre} | Edad {colono.edad} | Nivel {colono.nivel} | "
               if colono.esta_explorando():
                    texto += f"Explorando (vuelve en {colono.exploracion_restante} eventos)"
                    self._boton_menu(contenedor, texto)
               elif colono.ocupado:
                    self._boton_menu(contenedor, texto + "Ocupado")
               else:
                    texto += "En la colonia → Enviar de exploración"
                    self._boton_menu(contenedor, texto, lambda c=colono: self.enviar_exploracion(c))

     def enviar_exploracion(self, colono):
          # Sin ventana de aviso: la salida ya se ve en el registro y en el propio menu ("Explorando...")
          colono.irDeExploracion(self.colonia)
          self._refrescar_ya()

     def _refrescar_ya(self):
          if self._id_refresco is not None:
               self._raiz().after_cancel(self._id_refresco)
          self._refrescar_menu()

     # ---------- Recursos (tooltip) ----------
     # Color de cada recurso en la tarjeta (los que no esten aqui usan COLOR_RECURSO_DEFECTO)
     COLORES_RECURSOS = {
          "Madera": "#b07840",
          "Piedra": "#9e9e9e",
          "Agua": "#42a5f5",
          "Hierro": "#78909c",
          "Comida": "#ffb74d",
          "Plutonio": "#76ff03",
          "Semillas": "#d9b26f",
          "Plantas": "#66bb6a",
          "Moral": "#f06292",
          "Defensa": "#ef5350",
     }
     COLOR_RECURSO_DEFECTO = "#90caf9"
     FONDO_TARJETA = Tema.PANEL
     FONDO_CABECERA = Tema.CABECERA
     ANCHO_BARRA = 110

     @staticmethod
     def _formatear_cantidad(cantidad) -> str:
          # Algunas infraestructuras suman decimales (10 * eficiencia/100); mostramos enteros si se puede
          if isinstance(cantidad, float) and not cantidad.is_integer():
               return f"{cantidad:.1f}"
          return str(int(cantidad))

     def mostrarRecursos(self, evento):
          if not self.mostrar_subventana(evento):
               return
          tarjeta = tk.Frame(self.estoyEnLaVentana, bg=self.FONDO_TARJETA, highlightbackground=Tema.BORDE, highlightthickness=2)
          tarjeta.pack()

          tk.Label(
               tarjeta, text=f"Almacén de {self.colonia.nombre}", bg=self.FONDO_CABECERA, fg=Tema.TEXTO,
               font=("Arial", 11, "bold"), padx=12, pady=6,
          ).grid(row=0, column=0, columnspan=4, sticky="ew")

          recursos = dict(self.colonia.recursos)  # copia: el hilo de eventos puede modificarlos
          if not recursos:
               tk.Label(tarjeta, text="El almacén está vacío.", bg=self.FONDO_TARJETA, fg=Tema.TEXTO_SUAVE,
                        font=("Arial", 10, "italic"), padx=12, pady=10).grid(row=1, column=0, columnspan=4)
               return

          maximo = max(max(recursos.values()), 1)
          for fila, (tipo, cantidad) in enumerate(recursos.items(), start=1):
               color = self.COLORES_RECURSOS.get(tipo, self.COLOR_RECURSO_DEFECTO)
               vacio = cantidad <= 0
               color_texto = Tema.TEXTO_APAGADO if vacio else Tema.TEXTO
               pady = (8 if fila == 1 else 2, 8 if fila == len(recursos) else 2)

               # Punto de color
               punto = tk.Canvas(tarjeta, width=12, height=12, bg=self.FONDO_TARJETA, highlightthickness=0)
               punto.create_oval(1, 1, 11, 11, fill=color if not vacio else Tema.TEXTO_APAGADO, outline="")
               punto.grid(row=fila, column=0, padx=(12, 6), pady=pady)

               # Nombre
               tk.Label(tarjeta, text=tipo, bg=self.FONDO_TARJETA, fg=color_texto, font=("Arial", 10), anchor="w"
                        ).grid(row=fila, column=1, sticky="w", pady=pady)

               # Cantidad alineada a la derecha
               tk.Label(tarjeta, text=self._formatear_cantidad(cantidad), bg=self.FONDO_TARJETA, fg=color_texto,
                        font=("Arial", 10, "bold"), anchor="e", width=6
                        ).grid(row=fila, column=2, sticky="e", padx=(8, 8), pady=pady)

               # Barra proporcional al recurso del que mas hay
               barra = tk.Canvas(tarjeta, width=self.ANCHO_BARRA, height=8, bg=self.FONDO_TARJETA, highlightthickness=0)
               barra.create_rectangle(0, 0, self.ANCHO_BARRA, 8, fill=Tema.BARRA_VACIA, outline="")
               relleno = int(self.ANCHO_BARRA * max(cantidad, 0) / maximo)
               if relleno > 0:
                    barra.create_rectangle(0, 0, relleno, 8, fill=color, outline="")
               barra.grid(row=fila, column=3, padx=(0, 12), pady=pady)

          self._ajustar_posicion_subventana()

     # ---------- Infraestructuras ----------
     def abrir_menu_infraestructuras(self, evento):
          self._abrir_menu(evento, self._firma_infraestructuras, self._construir_menu_infraestructuras)

     def _firma_infraestructuras(self):
          # Se redibuja si cambia una infraestructura o los recursos (para activar/desactivar botones)
          infra = tuple((id(i), i.eficiencia, i.nivel) for i in self.colonia.infraestructuras)
          return infra, tuple(sorted(self.colonia.recursos.items()))

     @staticmethod
     def _texto_coste(coste: dict) -> str:
          return ", ".join(f"{cantidad} {recurso}" for recurso, cantidad in coste.items())

     def _construir_menu_infraestructuras(self, contenedor):
          if not self.colonia.infraestructuras:
               self._boton_menu(contenedor, "No hay infraestructuras.")
               return
          tk.Label(contenedor, text="Invertir: sube de nivel, produce más y la deja al 100%",
                   font=("Arial", 9, "italic"), fg=Tema.TEXTO_SUAVE).pack(fill=tk.X)
          recursos = self.colonia.recursos
          for infraestructura in self.colonia.infraestructuras:
               fila = tk.Frame(contenedor, bg=Tema.PANEL, padx=8, pady=6)
               fila.pack(fill=tk.X, pady=2)

               color_eficiencia = Tema.TEXTO if infraestructura.eficiencia > 0 else "#ff6b6b"
               tk.Label(fila, text=f"{infraestructura.tipo}", bg=Tema.PANEL, font=("Arial", 10, "bold")
                        ).grid(row=0, column=0, sticky="w")
               tk.Label(fila, text=f"Nv {infraestructura.nivel}/{infraestructura.MAX_NIVEL}  ·  Eficiencia {infraestructura.eficiencia}%",
                        bg=Tema.PANEL, fg=color_eficiencia).grid(row=0, column=1, sticky="w", padx=(10, 0))

               botones = tk.Frame(fila, bg=Tema.PANEL)
               botones.grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 0))

               if infraestructura.puede_invertir():
                    coste = infraestructura.coste_inversion()
                    boton = tk.Button(botones, text=f"Invertir ({self._texto_coste(coste)})",
                                      command=lambda i=infraestructura: self.invertir(i))
                    if not infraestructura._hay_recursos(recursos, coste):
                         boton.config(state=tk.DISABLED)
               else:
                    boton = tk.Button(botones, text="Nivel máximo", state=tk.DISABLED)
               boton.pack(side=tk.LEFT, padx=(0, 6))

               if infraestructura.eficiencia < 100:
                    coste = infraestructura.coste_reparacion()
                    boton = tk.Button(botones, text=f"Reparar ({self._texto_coste(coste)})",
                                      command=lambda i=infraestructura: self.reparar(i))
                    if not infraestructura._hay_recursos(recursos, coste):
                         boton.config(state=tk.DISABLED)
                    boton.pack(side=tk.LEFT, padx=(0, 6))

               if isinstance(infraestructura, Infraestructura.Huerto):
                    tk.Button(botones, text="Abrir huerto", command=lambda h=infraestructura: self.abrir_huerto(h)
                              ).pack(side=tk.LEFT)

               if isinstance(infraestructura, Infraestructura.NaveEspacial):
                    tk.Button(botones, text="Abrir menu de la nave", command=lambda n=infraestructura: self.abrir_menu_nave(n)
                              ).pack(side=tk.LEFT)

     def invertir(self, infraestructura):
          infraestructura.invertir(self.colonia.recursos)
          self._refrescar_ya()

     def reparar(self, infraestructura):
          infraestructura.reparar(self.colonia.recursos)
          self._refrescar_ya()

     def abrir_huerto(self, huerto):
          self.cerrar_subventana()
          VentanaHuerto(self.ventana, self.colonia, huerto)

     def abrir_menu_nave(self, nave):
          self.cerrar_subventana()
          VentanaNave(self.ventana, self.colonia, nave, self.colonias)

     # ---------- Construccion ----------
     def abrir_menu_construccion(self, evento):
          self._abrir_menu(evento, self._firma_construccion, self._construir_menu_construccion)

     def _firma_construccion(self):
          return tuple(sorted(self.colonia.recursos.items()))

     def _construir_menu_construccion(self, contenedor):
          texto_costes = Infraestructura.Infraestructura.mostrar_todos_costes()
          for linea in texto_costes.splitlines():
               if linea.strip():
                    tipo = linea.split()[0]
                    coste = Infraestructura.Infraestructura.COSTES.get(tipo, {})
                    texto = linea.strip()
                    if Infraestructura.Infraestructura._hay_recursos(self.colonia.recursos, coste):
                         self._boton_menu(contenedor, texto, lambda item=texto: self.nueva_infraestructura(item))
                    else:
                         # sin recursos suficientes: desactivado y mas apagado
                         self._boton_menu(contenedor, texto).config(disabledforeground=Tema.TEXTO_APAGADO)

     def nueva_infraestructura(self, linea):
          tipo = linea.split()[0]
          self.colonia.crear_infraestructuras(tipo)
          self._refrescar_ya()
