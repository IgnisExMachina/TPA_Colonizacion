import json
import logging
from pathlib import Path

from Colonia import Colonia
from Colono import Colono
from Infraestructura.Castillo import Castillo
from Infraestructura.Granja import Granja
from Infraestructura.Muralla import Muralla
from Infraestructura.Puente import Puente
from Infraestructura.Mina import Mina

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

CLASES_REGISTRADAS = {
    "Colonia": Colonia,
    "Colono": Colono,
    "Castillo": Castillo,
    "Granja": Granja,
    "Muralla": Muralla,
    "Puente": Puente,
    "Mina": Mina,
}

class GestorPersistencia:
    def __init__(self, ruta_archivo: str = "partidas/colonias_save.json"):
        self.ruta = Path(ruta_archivo)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

    def _a_diccionario(self, obj):
        if isinstance(obj, list):
            return [self._a_diccionario(elemento) for elemento in obj]
        
        if isinstance(obj, dict):
            return {clave: self._a_diccionario(valor) for clave, valor in obj.items()}

        if hasattr(obj, "__dict__"):
            datos = {}
            for clave, valor in obj.__dict__.items():
                # Limpiamos nombres internos si empiezan por _ para guardarlos limpios en el JSON
                nombre_limpio = clave[1:] if clave.startswith("_") and not clave.startswith("__") else clave
                
                if nombre_limpio.startswith("eventos") or nombre_limpio.startswith("timer"):
                    continue
                datos[nombre_limpio] = self._a_diccionario(valor)
            
            datos["__clase__"] = obj.__class__.__name__
            return datos

        return obj

    def _desde_diccionario(self, datos):
        if isinstance(datos, list):
            return [self._desde_diccionario(elemento) for elemento in datos]

        if isinstance(datos, dict):
            if "__clase__" in datos:
                datos_copia = datos.copy()
                nombre_clase = datos_copia.pop("__clase__")
                clase_python = CLASES_REGISTRADAS.get(nombre_clase)

                if clase_python is None:
                    raise ValueError(f"Clase desconocida en el guardado: {nombre_clase}")

                # Creamos la instancia vacía
                instancia = clase_python.__new__(clase_python)
                
                # Asignamos los atributos usando setattr para que dispare los setters de las properties
                for k, v in datos_copia.items():
                    valor_reconstruido = self._desde_diccionario(v)
                    try:
                        setattr(instancia, k, valor_reconstruido)
                    except AttributeError:
                        # Fallback por seguridad si alguna propiedad fuera de solo lectura
                        instancia.__dict__[k] = valor_reconstruido
                        
                return instancia
            
            return {clave: self._desde_diccionario(valor) for clave, valor in datos.items()}

        return datos

    def guardar_colonias(self, colonias: dict | list) -> None:
        try:
            datos_json = self._a_diccionario(colonias)
            with self.ruta.open("w", encoding="utf-8") as f:
                json.dump(datos_json, f, indent=4, ensure_ascii=False)
            logger.info(f"Colonias guardadas con éxito en {self.ruta}")
        except OSError as e:
            logger.error(f"Error de disco al guardar colonias: {e}")
            raise

    def cargar_colonias(self) -> dict | list:
        if not self.ruta.exists():
            logger.warning(f"No hay archivo de guardado previo en {self.ruta}")
            raise FileNotFoundError(f"No existe partida en {self.ruta}")

        try:
            with self.ruta.open("r", encoding="utf-8") as f:
                datos_leidos = json.load(f)
            colonias = self._desde_diccionario(datos_leidos)
            logger.info(f"Colonias cargadas correctamente desde {self.ruta}")
            return colonias
        except json.JSONDecodeError as e:
            logger.error(f"El archivo JSON está dañado: {e}")
            raise ValueError("El archivo de partida está corrupto.") from e