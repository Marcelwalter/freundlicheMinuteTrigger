#!/bin/zsh

# Umbennen des Terminal Fensters um es später schließen zu können
echo -n -e "\033]0;Companionscript\007"

# Pfad des aktuellen Shell-Skripts ermitteln
SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" &> /dev/null && pwd)

# Aktiviert die virtuelle Umgebung
source "$SCRIPT_DIR/.venv/bin/activate"

# Führt das Python-Skript mit den angegebenen Parametern aus
python3 "$SCRIPT_DIR/main.py" "$@"

# Deaktiviert die virtuelle Umgebung
deactivate

# mit diesem Befehl wird in Companion das letzte Fenster geschlossen
# osascript -e 'tell application "Terminal" to close (every window whose name contains "Companionscript")' &

exit

# Mit folgender Expression kann in Companion das Script ausgeführt werden:
# osascript -e 'tell application "Terminal" to do script "~/Desktop/FreundlicheMinute/FreundlicheMinute.sh 10:28; exit"'