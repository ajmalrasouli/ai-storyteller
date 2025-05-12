import sys
import os
from pathlib import Path

# Add backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))
