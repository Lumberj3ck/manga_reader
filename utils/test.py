import django, os
import sys
from pathlib import Path

# Add the parent directory (manga_reader) to the sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_reader.settings_prod")
django.setup()
from reader.models import *