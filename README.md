###  FreundlicheMinute Trigger Script

Dieses Python-Skript ermöglicht es, eine spezifische Präsentation in ProPresenter zur vorgegebenen Zeit automatisch zu starten. Es stellt sicher, dass nur eine Instanz des Skripts gleichzeitig ausgeführt wird, und setzt zusätzlich einen Countdown-Timer in ProPresenter.

## Voraussetzungen

1. **Python 3.7+** muss installiert sein.
2. Git sollte installiert sein.
3. Das Skript nutzt die ProPresenter API, die auf dem gleichen Rechner wie das Skript läuft oder über eine IP-Adresse erreichbar ist.

## Installation

1. **Klonen oder herunterladen** des Repositories:
   ```bash
   git clone <repository-url>
   ```
   oder den Quellcode direkt auf deinen Rechner kopieren.

2. **Virtuelle Umgebung einrichten** (empfohlen):
   ```bash
   python3 -m venv .venv
   source venv/bin/activate
   ```

3. **Abhängigkeiten installieren**:
   ```bash
   pip3 install -r requirements.txt
   ```
4. **Skript ausführbar machen**

   ```bash
   chmod +x freundlicheMinute.sh
   ```
5. **Skript ausführen**
   ```bash
   ./freundlicheMinute.sh 11:28 -bp Gottesdienst -n FreundlicheMinute -t "Freundliche Minute" -np 1025
   ```

## Verwendung

### Syntax

Das Skript erfordert mindestens einen Pflichtparameter (die Zeit) und bietet mehrere optionale Parameter:

```bash
python main.py <time> [options]
```

### Pflichtparameter

- **`time`**: Die Uhrzeit, zu der die Präsentation gestartet werden soll, im Format `HH:MM`. Beispiel: `11:28`.

### Optionale Parameter

- **`-bp, --backupplaylist`**: Name der Playlist, falls keine aktive Playlist gefunden wird. Standard: `Gottesdienst`.
- **`-n, --name`**: Name der Präsentation, die gestartet werden soll. Standard: `FreundlicheMinute`.
- **`-t, --timer`**: Name des Timers, der gestartet werden soll. Standard: `Freundliche Minute`.
- **`-np, --networkport`**: Netzwerkport, auf dem ProPresenter Control zuhört. Standard: `1025`.
- **`-i, --ip`**: IP-Adresse, auf dem ProPresenter installiert ist. Standard: `10.0.30.2`.

### Beispiele

1. **Einfaches Beispiel:**
   ```bash
   python main.py 11:28
   ```
   Dieses Beispiel startet die Präsentation `FreundlicheMinute` um `11:28` und setzt den Timer `Freundliche Minute` bis zu dieser Uhrzeit.

2. **Mit Backup-Playlist:**
   ```bash
   python main.py 11:28 -bp AlternativePlaylist
   ```
   Falls keine aktive Playlist vorhanden ist, wird `AlternativePlaylist` verwendet.

3. **Mit benutzerdefiniertem Präsentations- und Timer-Namen:**
   ```bash
   python main.py 11:28 -n "MeinePräsentation" -t "Mein Timer"
   ```

4. **Mit benutzerdefiniertem Netzwerkport:**
   ```bash
   python main.py 11:28 -np 1234
   ```

### PID-Handling

Das Skript verwaltet einen PID-Datei-Mechanismus, um sicherzustellen, dass immer nur eine Instanz des Skripts zur gleichen Zeit ausgeführt wird. Bei jedem Start versucht es, eine ältere Instanz des Skripts zu beenden, bevor es sich selbst ausführt.

## Fehlerbehebung

- **"No such process running!"**: Das Skript versucht, einen nicht mehr existierenden Prozess zu beenden. Dies ist normalerweise kein Grund zur Sorge.
- **"Specified time has already passed."**: Die angegebene Uhrzeit liegt in der Vergangenheit. Das Skript wird in diesem Fall nicht ausgeführt.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der Datei [LICENSE](LICENSE).
