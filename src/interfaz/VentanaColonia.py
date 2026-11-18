import tkinter as tk
from Colonia import Colonia
import Infraestructura

class VentanaColonia:
     def __init__(self, ventana_padre, colonia: Colonia):
          self.colonia = colonia
          self.estoyEnLaVentana = None
        
          # Creamos la ventana hija
          self.ventana = tk.Toplevel(ventana_padre)
          self.ventana.title("Estado del planeta")
          self.ventana.geometry("400x400")

          tk.Label(self.ventana, text=f"Nombre de la colonia: {self.colonia.nombre}", font=("Arial", 11, "bold")).pack(pady=10)
        
          botonVerColonos = tk.Button(self.ventana, text="Ver población actual")
          botonVerColonos.pack(pady=10)

          # Como ya tenemos self.colonia guardado arriba, no hace falta usar lambda
          botonVerColonos.bind("<Enter>", self.mostrarColonos)
          botonVerColonos.bind("<Leave>", self.ocultar_subventana)

          botonVerRecursos = tk.Button(self.ventana, text= "Ver recursos")
          botonVerRecursos.pack(pady=10)

          botonVerRecursos.bind("<Enter>", self.mostrarRecursos)
          botonVerRecursos.bind("<Leave>", self.ocultar_subventana)

          botonVerInfraestructuras = tk.Button (self.ventana, text = "Ver infraestructuras")
          botonVerInfraestructuras.pack(pady=10)

          botonVerInfraestructuras.bind("<Enter>", self.mostrar_infraestructuras)
          botonVerInfraestructuras.bind("<Leave>", self.ocultar_subventana)

          botonMenuInfraestructuras = tk.Button(self.ventana, text = "Menú de construcción")
          botonMenuInfraestructuras.pack(pady=10)

          botonMenuInfraestructuras.bind("<Button-1>", self.abrir_menu_construccion)
          #Mostrar las infraestructuras y sus costes. si se pueden construir, poder hacerlo.

          #tk.Label(self.ventana, text=f"Evento actual: {next(self.colonia._stream)}").pack(pady=10)
          tk.Button(self.ventana, text="Cerrar ventana", command=self.ventana.destroy).pack(pady=20)

     def mostrar_subventana(self, evento):
          if self.estoyEnLaVentana:
               return None
          self.estoyEnLaVentana = tk.Toplevel(self.ventana)
          self.estoyEnLaVentana.wm_overrideredirect(True)
          
          x = evento.x_root + 15
          y = evento.y_root + 15
          self.estoyEnLaVentana.geometry(f"+{x}+{y}")

     def ocultar_subventana(self, evento):
          if self.estoyEnLaVentana:
               self.estoyEnLaVentana.destroy()
               self.estoyEnLaVentana = None

     def mostrarColonos(self, evento):
          self.mostrar_subventana(evento)
          textoColonos = ""
          for colono in self.colonia.colonos:
               textoColonos += f"Nombre: {colono.nombre}\n"
               textoColonos += f"Edad: {colono.edad}\n"
               textoColonos += f"Está ocupado: {colono.ocupado}\n"
               textoColonos += "-------------------------\n"

          if not textoColonos:
               textoColonos = "No hay colonos registrados.\n"

          # Ponemos el texto en la ventanita
          tk.Label(self.estoyEnLaVentana, text=textoColonos, bg="#ffffe0", relief="solid", borderwidth=1, padx=8, pady=5).pack()

     def mostrarRecursos(self, evento):
          self.mostrar_subventana(evento)
          textoRecursos = ""
          for tipo, cantidad in self.colonia.recursos.items():
               textoRecursos += f"- {tipo} = {cantidad}\n"
               
          if not textoRecursos:
                    textoRecursos = "El almacén está vacío.\n"
          
          # Ponemos el texto en la ventanita
          tk.Label(self.estoyEnLaVentana, text=textoRecursos, bg="#f5be91", relief="solid", borderwidth=1, padx=8, pady=5).pack()
         
     def mostrar_infraestructuras(self, evento):
          self.mostrar_subventana(evento)
          textoInfraestructuras = ""
          for infraestructura in self.colonia.infraestructuras:
               textoInfraestructuras += f"Tipo: {infraestructura.tipo}\n"
               textoInfraestructuras += f"Eficiencia: {infraestructura.eficiencia}\n"
          if not textoInfraestructuras:
               textoInfraestructuras = "No hay infraestructuras.\n"
          
          tk.Label(self.estoyEnLaVentana, text=textoInfraestructuras, bg="#027a14", relief="solid", borderwidth=1, padx=8, pady=5).pack()

     def abrir_menu_construccion(self, evento):
          self.mostrar_subventana(evento)
          texto_costes = Infraestructura.Infraestructura.mostrar_todos_costes()
          lineas = texto_costes.splitlines()
          for linea in lineas:
               if linea.strip():
                    btn = tk.Button(
                         self.estoyEnLaVentana,
                         text=linea,
                         bg="#301a80",
                         fg="white",
                         relief="solid",
                         anchor="w",
                         command=lambda item=linea: self.nueva_infraestructura(item)
                    )
                    btn.pack(fill=tk.X, expand=True)
          tk.Button(self.estoyEnLaVentana, text="Cerrar ventana", command=self.estoyEnLaVentana.destroy).pack(pady=5)

     def nueva_infraestructura(self, linea):
          tipo = linea.split()[0]
          self.colonia.crear_infraestructuras(tipo)

