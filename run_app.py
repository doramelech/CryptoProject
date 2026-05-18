import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent
interface_path = project_dir / "INTERFACE.py"

try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(interface_path)], cwd=project_dir)
except Exception as e:
    print(f"App has ended")

