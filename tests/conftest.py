import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

for ruta in (str(ROOT), str(SRC)):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)