#!/bin/zsh

# Pfad des aktuellen Shell-Skripts ermitteln
SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" &> /dev/null && pwd)

# Aktiviert die virtuelle Umgebung
source "$SCRIPT_DIR/.venv/bin/activate"

# Führt das Python-Skript mit den angegebenen Parametern aus
python "$SCRIPT_DIR/main.py" "$@"

# Deaktiviert die virtuelle Umgebung
deactivate

# Terminal-Fenster schließen
exit

### Mit folgender Expression kann in Companion das Script ausgeführt werden:
### osascript -e 'tell application "Terminal" to do script "~/Desktop/FreundlicheMinute/FreundlicheMinute.sh 10:28; exit"'