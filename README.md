# Simulador de Colonización Espacial

Juego de simulación y gestión de recursos para colonizar planetas, escrito en Python con programación orientada a objetos, interfaz gráfica en Tkinter y eventos concurrentes.

Proyecto de la asignatura **Técnicas de Programación Avanzada** (Grado en Ingeniería Informática, Universidad Nebrija, grupo 6, Planetas).


## Descripción

La galaxia tiene tres planetas. En cada uno puede vivir una colonia con sus colonos, sus recursos y sus infraestructuras. Cada colonia funciona **en paralelo**, en su propio hilo, y recibe cada 10-30 segundos un evento aleatorio (tormentas, ataques enemigos, visitas, averías y, muy rara vez, un meteorito) que cambia su estado.

El jugador decide cómo responder: construir infraestructuras, invertir en ellas para subirlas de nivel, repararlas, enviar colonos de exploración, cultivar el huerto o construir una nave para fundar una colonia en un planeta libre.

Todo lo que ocurre se ve en el panel **Registro de la galaxia**, con colores según el tipo de mensaje, y también en la terminal. La partida se guarda automáticamente en JSON al cerrar la ventana y se carga al volver a abrir el juego.

## Funcionalidades

- **Tres planetas y colonias concurrentes**: cada colonia procesa sus eventos en su propio hilo.
- **Eventos aleatorios** con 5 niveles de severidad:
  - *Tormenta*: consume recursos.
  - *Enemigos*: mueren colonos (los que están explorando se libran).
  - *Visitas*: se unen colonos nuevos.
  - *Avería*: baja la eficiencia de una infraestructura o la destruye.
  - *Meteorito*: destruye la colonia y deja el planeta libre.
- **Colonos**: con nombre, edad, nivel y género. Se les puede enviar a explorar: vuelven a los 5 eventos con semillas, madera, agua o piedra (más cuanto mayor sea su nivel).
- **Recursos**: madera, piedra, agua, hierro, comida, plutonio, semillas y plantas, mostrados con barras en el almacén.
- **9 infraestructuras**: Granja, Mina, Aserradero, Pozo, Extractor de plutonio, Muralla, Castillo, Huerto y Nave espacial.
  - Cada una tiene un coste, produce en cada evento y pierde un 10 % de eficiencia.
  - Se puede **invertir** en ellas (hasta el nivel 5, produce más) o **repararlas** (vuelven al 100 %).
- **Huerto**: plantar semillas, verlas crecer durante 5 eventos y recoger plantas y semillas nuevas.
- **Nave espacial**: con tripulación, plantas y plutonio sale a fundar una colonia en un planeta libre.
- **Persistencia**: guardado y carga automáticos en `src/partidas/colonias_save.json`.

## Estructura del repositorio

```
TPA_Colonizacion/
├── src/
│   ├── main.py                    # Punto de entrada
│   ├── Colonia.py                 # Estado de la colonia y procesado concurrente de eventos
│   ├── Colono.py                  # Colonos (propiedades validadas, exploración)
│   ├── Planeta.py                 # Planeta y fundación de colonias
│   ├── GestorPersistencia.py      # Guardado/carga de la partida en JSON
│   ├── eventos/
│   │   ├── Evento.py              # Evento (tipo + severidad → título)
│   │   └── GestorEventos.py       # Genera eventos con un temporizador (threading.Timer)
│   ├── Infraestructura/
│   │   ├── Infraestructura.py     # Clase base: costes, construir, invertir, reparar
│   │   ├── Granja.py, Mina.py, Aserradero.py, Pozo.py,
│   │   ├── ExtractorDePlutonio.py, Muralla.py, Castillo.py
│   │   ├── Huerto.py              # Plantar, crecer y recoger
│   │   └── NaveEspacial.py        # Tripulación y requisitos de despegue
│   ├── interfaz/
│   │   ├── Interfaz.py            # Ventana principal: galaxia y planetas
│   │   ├── VentanaColonia.py      # Población, recursos, infraestructuras y construcción
│   │   ├── VentanaFundar.py       # Fundar una colonia en un planeta libre
│   │   ├── VentanaHuerto.py       # Huerto dibujado en un Canvas
│   │   ├── VentanaNave.py         # Elegir planeta y despegar
│   │   ├── Registro.py            # Panel de registro (stdout → cola → Tkinter)
│   │   └── Tema.py                # Colores comunes de la interfaz
│   ├── imagenesPlanetas/          # Fondo y planetas
│   └── partidas/colonias_save.json
├── tests/                         # Pruebas con pytest (78 casos)
├── entrega/                       # Memoria, presentación y capturas de la entrega final
├── requirements.txt
└── pytest.ini
```

## Arquitectura

- `Interfaz` guarda un diccionario `colonias` con una `Colonia` por planeta.
- Cada `Colonia` agrega colonos e infraestructuras y tiene su propio `GestorEventos`.
- Todas las infraestructuras heredan de `Infraestructura` y redefinen `aplicar_efecto()`. La colonia las recorre sin preocuparse del tipo (polimorfismo).

**Concurrencia**:
- Un `threading.Timer` mete eventos en una `queue.Queue`.
- El hilo de la colonia los saca y los aplica.
- Los `print` van a una cola que el hilo de Tkinter lee con `after()`. Así ningún hilo secundario toca la interfaz, que en Tkinter no es segura entre hilos.


## Instalación y ejecución

**Requisitos:** Python **3.10 o superior** (se usa `match` y tipos `X | None`), con `tkinter` incluido. En Debian/Ubuntu: `sudo apt install python3-tk`.

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/IgnisExMachina/TPA_Colonizacion.git
   cd TPA_Colonizacion
   ```

2. Crear y activar un entorno virtual:

   ```bash
   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instalar las dependencias (Pillow y pytest):

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar el juego desde la raíz del repositorio:

   ```bash
   python src/main.py
   ```

5. Ejecutar los tests:

   ```bash
   pytest
   ```

   `pytest.ini` añade `src` a las rutas de búsqueda para que los tests importen igual que el programa.

> **Velocidad de los eventos:** se cambia con `MIN` y `MAX` en `src/eventos/GestorEventos.py`. Si borras `src/partidas/colonias_save.json`, el juego empieza con las tres colonias por defecto.

## Guía rápida de uso

1. **Haz clic en un planeta.** Si tiene colonia se abre su ventana; si está libre, puedes fundar una nueva.
2. **Ver población actual**: lista de colonos. Pulsa uno para enviarlo de exploración.
3. **Ver recursos** (hover con ratón): almacén con barras.
4. **Ver infraestructuras**: nivel y eficiencia de cada una, con los botones *Invertir*, *Reparar*, *Abrir huerto* y *Abrir menú de la nave*.
5. **Menú de construcción**: solo se activan las infraestructuras que puedes pagar.
6. **Registro de la galaxia**: sigue los eventos de todas las colonias. Se puede ocultar o limpiar.
7. **Cierra la ventana principal** para guardar la partida.


## Tecnologías

- **Lenguaje:** Python 3.10+
- **Paradigma:** programación orientada a objetos
- **Interfaz:** Tkinter y Pillow
- **Concurrencia:** `threading` y `queue`
- **Persistencia:** JSON
- **Pruebas:** pytest

## Licencia

Este proyecto se distribuye bajo los términos de la licencia detallada en el archivo [LICENSE](LICENSE).

## Contribuidores

Proyecto desarrollado por: Mateo Guinsburg, Aitor Casares, Ignacio Compaired y Daniel Ortiz.

<a href="https://github.com/IgnisExMachina/TPA_Colonizacion/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=IgnisExMachina/TPA_Colonizacion" alt="Contribuidores del proyecto" />
</a>
