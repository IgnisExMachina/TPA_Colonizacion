"""Colores comunes de toda la interfaz (azul oscuro).

Si quereis cambiar el aspecto del juego, basta con tocar los colores de aqui:
todas las ventanas los cogen de este archivo.
"""

FONDO = "#0b1730"           # * fondo de todas las ventanas
PANEL = "#12224a"           # * tarjetas, menus y campos de texto
CABECERA = "#1c3566"        # * titulos de tarjetas y paneles
BOTON = "#1c3566"
BOTON_ACTIVO = "#2a4d8f"    # * boton con el raton encima / pulsado
BORDE = "#3e6ac9"
TEXTO = "#e8eefc"
TEXTO_SUAVE = "#93a7cc"     # * textos secundarios
TEXTO_APAGADO = "#5a6d94"   # * cosas desactivadas o a cero
BARRA_VACIA = "#1a2c55"     # * fondo de las barras de progreso


def aplicar_tema(raiz):
    """Pone los colores por defecto a todos los widgets que se creen despues.
    Hay que llamarla justo despues de crear la ventana principal (tk.Tk())."""
    raiz.configure(bg=FONDO)
    opciones = {
        "*Background": FONDO,
        "*Foreground": TEXTO,
        "*highlightBackground": FONDO,
        "*highlightColor": BORDE,
        "*Button.Background": BOTON,
        "*Button.Foreground": TEXTO,
        "*Button.activeBackground": BOTON_ACTIVO,
        "*Button.activeForeground": TEXTO,
        "*Button.disabledForeground": TEXTO_APAGADO,
        "*Button.relief": "flat",
        "*Button.padX": 10,
        "*Button.padY": 4,
        "*Button.cursor": "hand2",
        "*Entry.Background": PANEL,
        "*Entry.Foreground": TEXTO,
        "*Entry.insertBackground": TEXTO,
        "*Entry.relief": "flat",
        "*Entry.highlightThickness": 1,
        "*Entry.highlightBackground": BORDE,
        "*Scrollbar.Background": BOTON,
        "*Scrollbar.troughColor": FONDO,
        "*Scrollbar.activeBackground": BOTON_ACTIVO,
        "*Text.Background": PANEL,
        "*Text.Foreground": TEXTO,
    }
    for patron, valor in opciones.items():
        raiz.option_add(patron, valor)
