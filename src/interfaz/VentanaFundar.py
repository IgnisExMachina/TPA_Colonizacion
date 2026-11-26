import tkinter as tk
from Colonia import Colonia
from Colono import Colono

#todo: necesita dar a elegir entre SOLO las colonias que tengan naves espaciales para fundar la nueva, SOLO si existen colonias

class VentanaFundar():
    def __init__(self, ventanaPadre, coloniasExistentes: dict, key, colonosIniciales = None):
        self.coloniasExistentes = coloniasExistentes
        self.key = key
        self.colonosIniciales = colonosIniciales

        self.ventana = tk.Toplevel(ventanaPadre)
        self.ventana.title("Planeta no ocupado.")
        self.ventana.geometry("400x260")
        self.ventana.columnconfigure(1, weight=1)


        anterior = coloniasExistentes.get(key)
        if isinstance(anterior, Colonia) and anterior.abandonada:
            texto = f"Aquí estaba la colonia {anterior.nombre}, abandonada al quedarse sin colonos ni infraestructuras."
        elif isinstance(anterior, Colonia) and anterior.destruida:
            texto = f"Aquí estaba la colonia {anterior.nombre}, destruida por un meteorito."
        else:
            texto = "Este planeta está libre. ¡Funda una colonia!"
        tk.Label(self.ventana, text=texto, wraplength=360, font=("Arial", 10, "bold")
                 ).grid(row=0, column=0, columnspan=2, padx=10, pady=(12, 4))

        self.campos = {
            "Nombre Colonia": "",
            "Recursos adicionales": "0",
        }
        self.entradas = {}
        if not self.existen_colonias() or self.colonosIniciales is not None:
            self.campos = {
                "Nombre Colonia": "",
                "Recursos adicionales": "0",
            }

            for fila, (campo, valor_inicial) in enumerate(self.campos.items(), start=1):
                label = tk.Label(self.ventana, text=f"{campo}:")
                label.grid(row=fila, column=0, padx=10, pady=8, sticky="w")

                entrada = tk.Entry(self.ventana)
                entrada.insert(0, valor_inicial)
                entrada.grid(row=fila, column=1, padx=10, pady=8, sticky="ew")
                self.entradas[campo] = entrada

            botonFundar = tk.Button(self.ventana, text="Fundar Colonia", command=self.fundar_colonia)
            botonFundar.grid(row=len(self.campos) + 1, column=0, columnspan=2, pady=(15, 4))

            # Mensajes de error (nombre vacio, numero mal escrito...)
            self.etiquetaAviso = tk.Label(self.ventana, text="", fg="#ff6b6b")
            self.etiquetaAviso.grid(row=len(self.campos) + 2, column=0, columnspan=2)

            self.entradas["Nombre Colonia"].focus_set()
    def fundar_colonia(self):
        datos = {campo: entrada.get().strip() for campo, entrada in self.entradas.items()}

        nombre = datos["Nombre Colonia"]
        if not nombre:
            self.etiquetaAviso.config(text="La colonia necesita un nombre.")
            return

        try:
            adicionales = int(datos["Recursos adicionales"] or 0)
        except ValueError:
            self.etiquetaAviso.config(text="Recursos adicionales debe ser un número entero.")
            return
        if adicionales < 0:
            self.etiquetaAviso.config(text="Recursos adicionales no puede ser negativo.")
            return

        # Se suma la cantidad adicional a cada recurso base (salvo los que empiezan a 0, como el Plutonio)
        recursos = {tipo: cantidad + adicionales if cantidad > 0 else cantidad
                    for tipo, cantidad in Colonia.RECURSOS_BASE.items()}
        if self.colonosIniciales == None:
            colonia = Colonia(nombre=nombre, colonos=[Colono.aleatorio(nombre)], recursos=recursos)
            self.coloniasExistentes[self.key] = colonia
            colonia.iniciar_gestion()
            print(f"¡Se ha fundado la colonia {nombre}! Primer colono: {colonia.colonos[0].nombre}")
            self.ventana.destroy()
        else:
            colonia = Colonia(nombre=nombre, colonos=self.colonosIniciales, recursos=recursos)
            self.coloniasExistentes[self.key] = colonia
            colonia.iniciar_gestion()
            print(f"¡La tripulación ha fundado la colonia {nombre}!")
            self.ventana.destroy()

    def existen_colonias(self):
        for key in self.coloniasExistentes:
            if isinstance(self.coloniasExistentes[key], Colonia):
                return True
        return False