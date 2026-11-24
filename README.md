# Simulador de Colonización Espacial

Proyecto de simulación y gestión de recursos para la colonización de planetas en Python.

# Descripción del proyecto

La aplicación ha sido desarrollada en Python está orientada a la gestión de recursos, el aumento de población, la construcción de infraestructuras y toma de decisiones ante eventos aleatorios que irán ocurriendo en un tiempo aleatorio determinado.

El proyecto cuenta con una interfaz gráfica interactiva de una galaxia que permite al usuario supervisar el estado actual de cada planeta, su colonia y todo lo que hay dentro de ella; colonos, recursos, infraestructuras.

Las alertas de eventos se muestran en el panel "Registro de la galaxia" dentro de la propia interfaz (con colores según el tipo de mensaje) y también en la terminal.

# Características Principales del programa

- Exploración Planetaria: Distintos planetas generados de manera aleatoria con una cantidad fija de recursos en cada planeta.

- Gestión de Colonos: Asignación de roles dentro de la colonia y supervivencia en entornos hostiles.

- Infraestructura y Asentamientos: Construcción y mantenimiento de las infraestructuras.

- Economía de Recursos: Extracción, almacenamiento y consumo de recursos para la creación de infraestructuras.

- Sistema de Eventos: Generador aleatorio de eventos (enemigos, tormentas, visitas y averías).

- Interfaz Gráfica: App visual con planetas y seguimiento a tiempo real de lo que está pasando en la galaxia completa.

# Estructura del Repositorio

TPA_Colonizacion/
│
├── main.py                     # Punto de entrada: el programa se arranca desde aquí
├── Interfaz                
│   ├── Interfaz.py             # Interfaz gráfica de usuario (GUI)
│   ├── VentanaColonia.py       # Seguimos con la interfaz pero más concretamente en la parte hover y menú desplegable
│   ├── VentanaFundar.py        # Ventana para fundar una colonia en un planeta libre
│   ├── VentanaHuerto.py        # Ventana del huerto: plantar semillas y recoger la cosecha
│   ├── Registro.py             # Panel de registro: muestra con colores lo que se imprime en la terminal
├── Colonia.py                  # Lógica y estado de la colonia activa
├── Colono.py                   # Entidad y atributos individuales de los colonos
├── infraestructura             # Definición y costes de las infraestructuras
│   ├── Infraestructura.py      # Infraestructura general padre
│   ├── Castillo.py             # Infraestructura castillo
│   ├── Granja.py               # Infraestructura granja
│   ├── Mina.py                 # Infraestructura mina
│   ├── Muralla.py              # Infraestructura muralla
│   ├── Aserradero.py           # Infraestructura aserradero (produce madera)
│   ├── Pozo.py                 # Infraestructura pozo (produce agua)
│   ├── ExtractorDePlutonio.py  # Infraestructura extractor de plutonio (produce plutonio)
│   └── Huerto.py               # Infraestructura huerto (plantas y semillas, cada 5 eventos)
├── Planeta.py                  # Parámetros y condiciones ambientales de cada planeta
├── Evento.py                   # Definición de eventos aleatorios e incidentes
├── GestorEventos.py            # Gestor de eventos
│__ GestorPersistencia          # Gestor de persistencia en archivos JSON
├── imagenesPlanetas/           # Recursos gráficos de la interfaz
│   ├── fondo.jpeg              # Fondo general de la interfaz
│   ├── planetaA.png
│   ├── planetaB.png
│   ├── planetaC.png
│   └── planetaD.png
│
├── .gitignore
├── LICENSE
└── README.md


# Instalación y Puesta en Marcha

### Prerrequisitos

Python 3.8 o superior instalado en el sistema.

Dependencias gráficas (tkinter y Pillow).
Para instalar Pillow:

```bash
pip install Pillow
```

1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/TPA_Colonizacion.git
cd TPA_Colonizacion
```

2. Entorno virtual (opcional pero recomendado)

# En Linux/macOS

```bash
git clone https://github.com/tu-usuario/TPA_Colonizacion.git
python3 -m venv env
source env/bin/activate
```
y pulsamos el botón de correr

# En Windows

```bash
python -m venv env
env\Scripts\activate
```

3. Ejecutar el proyecto

Desde la carpeta raíz del repositorio:

```bash
python src/main.py
```

4. Instalación de dependencias

Con el entorno virtual activado, instala todo lo necesario (Pillow y pytest) de una vez:

```bash
pip install -r requirements.txt
```

5. Ejecutar los tests

Desde la carpeta raíz del repositorio:

```bash
pytest
```

La configuración está en `pytest.ini`, que añade `src` a las rutas de búsqueda para que los tests importen igual que el programa.


# Guía Rápida de Uso

Selecciona un planeta: Evalúa la disponibilidad de recursos y riesgos en la pantalla inicial.

Despliega la base inicial: Administra los colonos iniciales y asigna tareas prioritarias (energía, soporte vital, extracción).

Monitorea los balances: Evita el agotamiento de suministros críticos antes de expandir la colonia.

Responde a los eventos: Toma decisiones estratégicas cuando el GestorEventos alerte de emergencias climáticas o averías.

# Tecnologías Utilizadas

Lenguaje: Python 3

Paradigma: Programación Orientada a Objetos (POO)

Gráficos: Tkinter / Canva

# Licencia

Este proyecto se distribuye bajo los términos de la licencia detallada en el archivo LICENSE.

# Autoría y Agradecimientos

Proyecto desarrollado por: Mateo Guinsburg, Aitor Casares, Ignacio Compaired, Daniel Ortiz

## Contribuidores

<a href="https://github.com/IgnisExMachina/TPA_Colonizacion/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=IgnisExMachina/TPA_Colonizacion" alt="Contribuidores del proyecto" />
</a>
