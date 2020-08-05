import os
from pathlib import Path

PORT = int(os.getanv("PORT", 8000))
print(PORT)

CAHCE_AGE = 60 * 60 * 24

PROJECT_DIR = Path(__file__).parent.resolve()
