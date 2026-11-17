import tkinter as tk
from Colonia import Colonia

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
        botonVerColonos.bind("<Leave>", self.ocultarColonos)

        botonVerRecursos = tk.Button(self.ventana, text= "Ver recursos")
        botonVerRecursos.pack(pady=10)

        botonVerRecursos.bind("<Enter>", self.mostrarRecursos)
        botonVerRecursos.bind("<Leave>", self.ocultarRecursos)

        tk.Label(self.ventana, text=f"Evento actual: {next(self.colonia._stream)}").pack(pady=10)
        tk.Button(self.ventana, text="Cerrar ventana", command=self.ventana.destroy).pack(pady=20)

    def mostrarColonos(self, evento):
        # Si ya hay alguna ventana no se abre la nueva
        if self.estoyEnLaVentana is not None:
             return
             
        # Crea otra ventana secundaria flotante
        self.estoyEnLaVentana = tk.Toplevel(self.ventana)
        self.estoyEnLaVentana.wm_overrideredirect(True) # Quita los bordes
        
        # Posición relativa al ratón
        x = evento.x_root + 15
        y = evento.y_root + 15
        self.estoyEnLaVentana.geometry(f"+{x}+{y}")

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

    def ocultarColonos(self, evento):
         if self.estoyEnLaVentana:
              self.estoyEnLaVentana.destroy()
              self.estoyEnLaVentana = None


    def mostrarRecursos(self, evento):
         if self.estoyEnLaVentana is not None:
              return
         self.estoyEnLaVentana = tk.Toplevel(self.ventana)
         self.estoyEnLaVentana.wm_overrideredirect(True)

         # Posición relativa al ratón
         x = evento.x_root + 15
         y = evento.y_root + 15
         self.estoyEnLaVentana.geometry(f"+{x}+{y}")

         textoRecursos = ""
         for tipo, cantidad in self.colonia.recursos.items():
              textoRecursos += f"- {tipo} = {cantidad}\n"
          
         if not textoRecursos:
                  textoRecursos = "El almacén está vacío.\n"
         
         # Ponemos el texto en la ventanita
         tk.Label(self.estoyEnLaVentana, text=textoRecursos, bg="#f5be91", relief="solid", borderwidth=1, padx=8, pady=5).pack()
         
    def ocultarRecursos(self, evento):
         if self.estoyEnLaVentana:
            self.estoyEnLaVentana.destroy()
            self.estoyEnLaVentana = None