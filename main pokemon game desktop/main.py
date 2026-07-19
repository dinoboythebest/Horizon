import os
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))

import pokemon

if __name__ == "__main__":
    pokemon.main()
