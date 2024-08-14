#!/bin/zsh

# Pfad des aktuellen Shell-Skripts ermitteln
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Aktiviert die virtuelle Umgebung
source "$SCRIPT_DIR/venv/bin/activate"

# Führt das Python-Skript mit den angegebenen Parametern aus
python "$SCRIPT_DIR/script.py" "$@"

# Deactivate the virtual environment
deactivate