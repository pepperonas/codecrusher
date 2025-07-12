# 🚀 Setup & Installation Guide

## Quick Start (5 Minuten)

```bash
# 1. Setup ausführen
./scripts/setup.sh

# 2. Juice Shop starten
docker run -d -p 3000:3000 bkimminich/juice-shop

# 3. Alle Challenges lösen
./scripts/run_all.sh

# 4. Results anzeigen
open reports/*.html
```

## Detaillierte Installation

### Voraussetzungen prüfen

```bash
# Python Version (3.8+ erforderlich)
python3 --version

# Docker (für Juice Shop)
docker --version

# Git (für Repository)
git --version
```

### 1. Repository Setup

```bash
# Falls noch nicht geklont
git clone https://github.com/pepperonas/codecrusher.git
cd codecrusher

# Oder ZIP entpacken
unzip codecrusher.zip
cd codecrusher
```

### 2. Virtuelle Umgebung

```bash
# Erstellen
python3 -m venv venv

# Aktivieren (Linux/Mac)
source venv/bin/activate

# Aktivieren (Windows)
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt
```

### 3. OWASP Juice Shop starten

**Option A: Docker (empfohlen)**
```bash
docker run -d -p 3000:3000 --name juice-shop bkimminich/juice-shop
```

**Option B: NPM**
```bash
npm install -g juice-shop
juice-shop
```

**Option C: Heroku (Remote)**
```bash
# Nutze: http://juice-shop.herokuapp.com
# Kein lokaler Setup nötig
```

### 4. Konfiguration anpassen

```bash
# Kopiere und bearbeite Konfiguration
cp config/settings.yaml config/my-settings.yaml
nano config/my-settings.yaml
```

Wichtige Einstellungen:
```yaml
juice_shop:
  base_url: "http://localhost:3000"  # Anpassen falls nötig

selenium:
  headless: false  # Auf true für Server ohne GUI

exploitation:
  delay_between_attacks: 1  # Erhöhen bei langsamer Verbindung
```

### 5. Verbindung testen

```bash
cd src
python main.py --target http://localhost:3000 --category injection --verbose
```

## Verwendung

### Basis-Kommandos

```bash
# Alle Challenges automatisch lösen
python main.py --solve-all

# Nur bestimmte Kategorie
python main.py --category injection

# Educational Mode mit Erklärungen
python main.py --educational

# Mit Custom Config
python main.py --config ../config/my-settings.yaml --solve-all
```

### Erweiterte Optionen

```bash
# Verschiedene Targets
python main.py --target http://juice-shop.herokuapp.com --solve-all

# Report-Generierung
python main.py --solve-all --report html
python main.py --solve-all --report json

# Verbose Logging
python main.py --solve-all --verbose
```

### Convenience Scripts

```bash
# Setup komplett automatisch
./scripts/setup.sh

# Alle Challenges mit Report
./scripts/run_all.sh

# Nur Injection Attacks
./scripts/run_all.sh http://localhost:3000 html injection

# Educational Mode
./scripts/run_all.sh http://localhost:3000 html educational
```

## Troubleshooting

### Häufige Probleme

**Problem: `ModuleNotFoundError: No module named 'selenium'`**
```bash
# Lösung: Virtuelle Umgebung aktivieren
source venv/bin/activate
pip install -r requirements.txt
```

**Problem: `Connection refused to localhost:3000`**
```bash
# Lösung: Juice Shop starten
docker run -d -p 3000:3000 bkimminich/juice-shop

# Status prüfen
curl http://localhost:3000
```

**Problem: `ChromeDriver not found`**
```bash
# Lösung: WebDriver Manager installieren
pip install webdriver-manager

# Oder manuell ChromeDriver herunterladen
# https://chromedriver.chromium.org/
```

**Problem: Permission denied auf Skripten**
```bash
# Lösung: Ausführungsrechte setzen
chmod +x scripts/*.sh
```

**Problem: SSL Certificate Error**
```bash
# Lösung: SSL Verification deaktivieren (nur für lokale Tests)
# In config/settings.yaml:
security:
  verify_ssl: false
```

### Debug-Modus

```bash
# Detailliertes Logging
python main.py --solve-all --verbose --log-level DEBUG

# Screenshots bei Fehlern
python main.py --solve-all --screenshot-on-error

# Einzelnen Challenge debuggen
python main.py --category injection --challenge "Login Admin" --verbose
```

### Browser-Probleme

```bash
# Headless Mode für Server
python main.py --solve-all --headless

# Verschiedene Browser testen
python main.py --solve-all --browser firefox
python main.py --solve-all --browser edge
```

## Performance-Optimierung

### Parallel Execution
```bash
# Multiple Kategorien parallel (falls implementiert)
python main.py --solve-all --parallel 4
```

### Resource Limits
```yaml
# In config/settings.yaml
exploitation:
  delay_between_attacks: 0.5  # Schneller
  max_retry_attempts: 2       # Weniger Versuche
  timeout: 15                 # Kürzere Timeouts
```

## Erweiterte Konfiguration

### AI Integration (Optional)
```yaml
ai:
  enabled: true
  provider: "openai"
  api_key: "your-openai-key"
  model: "gpt-4"
```

### Proxy Setup
```yaml
security:
  proxy:
    enabled: true
    http: "http://proxy.company.com:8080"
    https: "https://proxy.company.com:8080"
```

### Custom Wordlists
```bash
# Erstelle custom Wordlists
mkdir custom-wordlists
echo -e "admin\npassword\nsecret" > custom-wordlists/passwords.txt

# In Python Code referenzieren
wordlist = open('custom-wordlists/passwords.txt').read().splitlines()
```

## Docker Setup (Alternative)

### Dockerfile erstellen
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

CMD ["python", "src/main.py", "--solve-all"]
```

### Docker Build & Run
```bash
# Build
docker build -t juice-automation .

# Run mit Volume für Reports
docker run -v $(pwd)/reports:/app/reports juice-automation

# Interactive Mode
docker run -it juice-automation python src/main.py --educational
```

## Nützliche Befehle

### Logs analysieren
```bash
# Tail Logs
tail -f logs/*.log

# Error-only Logs
grep ERROR logs/*.log

# Success Rate
grep -c "successful" logs/*.log
```

### Reports verwalten
```bash
# Neuesten Report öffnen
open $(ls -t reports/*.html | head -1)

# Reports archivieren
tar -czf reports-backup-$(date +%Y%m%d).tar.gz reports/

# Cleanup alte Reports
find reports/ -name "*.html" -mtime +7 -delete
```

### Performance Monitoring
```bash
# Resource Usage während Execution
top -p $(pgrep -f "python.*main.py")

# Network Traffic
netstat -i

# Disk Usage
du -sh reports/ logs/ screenshots/
```

## Support

### Log-Level für Support
```bash
# Vollständige Debug-Logs für Support-Anfragen
python main.py --solve-all --log-level DEBUG --verbose 2>&1 | tee support-debug.log
```

### Systeminformationen sammeln
```bash
# System Info
python --version > system-info.txt
pip list >> system-info.txt
docker --version >> system-info.txt
uname -a >> system-info.txt
```

---

**🎯 Nach erfolgreicher Installation: `./scripts/run_all.sh` für vollautomatische Challenge-Lösung!**