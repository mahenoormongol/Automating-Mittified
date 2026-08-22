import sys
import os
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.database.models import Analysis

try:
    a = Analysis(video_id=1, content_category="test")
    print("SUCCESS: Analysis instantiated with content_category")
except TypeError as e:
    print(f"FAILURE: {e}")
except Exception as e:
    print(f"UNEXPECTED ERROR: {e}")
