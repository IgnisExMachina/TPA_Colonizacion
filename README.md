# Simulador de Colonización Espacial

Proyecto de simulación y gestión de recursos para la colonización de planetas en Python.

# Descripción del proyecto

La aplicación ha sido desarrollada en Python está orientada a la gestión de recursos, el aumento de población, la construcción de infraestructuras y toma de decisiones ante eventos aleatorios que irán ocurriendo en un tiempo aleatorio determinado.

El proyecto cuenta con una interfaz gráfica interactiva de una galaxia que permite al usuario supervisar el estado actual de cada planeta, su colonia y todo lo que hay dentro de ella; colonos, recursos, infraestructuras y los eventos que están pasando dentro de ella.

# Características Principales del programa

- Exploración Planetaria: Distintos planetas generados de manera aleatoria con distintos recursos y recursos en cada uno de ellos.

- Gestión de Colonos: Asignación de roles dentro de la colonia y supervivencia en entornos hostiles.

- Infraestructura y Asentamientos: Construcción y mantenimiento de las infraestructuras.

- Economía de Recursos: Extracción, almacenamiento y consumo de recursos para la creación de infraestructuras.

- Sistema de Eventos: Generador aleatorio de eventos (enemigos y tormentas).

- Interfaz Gráfica: App visual con planetas y seguimiento a tiempo real de lo que está pasando en la galaxia completa.

# Estructura del Repositorio

TPA_Colonizacion/
│
├── Interfaz.py                # Interfaz gráfica de usuario (GUI)
├── Colonia.py                  # Lógica y estado de la colonia activa
├── Colono.py                   # Entidad y atributos individuales de los colonos
├── Infraestructura.py          # Definición y costes de las infraestructuras
├── Planeta.py                  # Parámetros y condiciones ambientales de cada planeta
├── Recursos.py                 # Modelo general de inventario y consumos
├── RecursosDelPlaneta.py       # Reservas naturales y tasas de extracción por planeta
├── Evento.py                   # Definición de eventos aleatorios e incidentes
├── GestorEventos.py            # Gestor de eventos
│
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

```bash
python interface.py
```

4. Instalación de Pillow

Como ya expliqué anteriormente, ya que instalar Pillow en la terminal para que el proyecto reconozca la librería correspondiente.


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
