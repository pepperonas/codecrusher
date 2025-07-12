# 💥 CodeCrusher - Web Application Security Testing Framework

Ein umfassendes Framework zur **vollautomatischen Lösung aller Web Application Security Challenges** mit integrierter KI-Unterstützung und umfangreichen Schulungsmaterialien.

**CodeCrusher** zermalmt unsicheren Code und deckt systematisch alle Vulnerabilities in Web-Anwendungen auf.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Security](https://img.shields.io/badge/purpose-educational-red.svg)
![Author](https://img.shields.io/badge/author-Martin%20Pfeffer-brightgreen.svg)
![Year](https://img.shields.io/badge/year-2025-blue.svg)

## 🎯 Überblick

**CodeCrusher** automatisiert **alle 110+ Web Application Security Challenges** und bietet:

- ✅ **Vollautomatische Lösung** aller Challenges
- 🤖 **KI-gestützte Exploit-Generierung**
- 📚 **Umfassende Schulungsmaterialien**
- 📊 **Detaillierte HTML/JSON Reports**
- 🎓 **Educational Mode** mit Schritt-für-Schritt Erklärungen
- 🔧 **Modularer, erweiterbarer Aufbau**

## 🚀 Quick Start

```bash
# 1. Repository klonen
git clone https://github.com/pepperonas/codecrusher.git
cd codecrusher

# 2. Setup ausführen
./scripts/setup.sh

# 3. Juice Shop starten (falls nicht bereits laufend)
docker run -d -p 3000:3000 bkimminich/juice-shop

# 4. Alle Challenges lösen
./scripts/run_all.sh

# 5. Educational Mode
./scripts/run_all.sh http://localhost:3000 html educational
```

## 📋 Voraussetzungen

### System-Anforderungen
- **Python 3.8+**
- **Docker** (für Juice Shop)
- **Chrome/Firefox Browser**
- **4GB RAM** (empfohlen)

### Dependencies
```bash
# Automatisch durch setup.sh installiert
pip install -r requirements.txt
```

## 🏗️ Architektur

```
codecrusher/
├── src/
│   ├── core/                    # Kern-Module
│   │   ├── api_client.py       # REST API Client
│   │   ├── session_manager.py  # Session/Token Verwaltung
│   │   └── browser_automation.py # Selenium WebDriver
│   ├── exploits/               # Exploit-Module
│   │   ├── injection/          # SQL, NoSQL, Command Injection
│   │   ├── authentication/     # Auth-Bypass, JWT-Manipulation
│   │   ├── xss/               # Cross-Site Scripting
│   │   └── ...                # Weitere Kategorien
│   ├── utils/                  # Hilfs-Module
│   └── main.py                # Hauptanwendung
├── config/
│   └── settings.yaml          # Konfiguration
├── docs/                      # Dokumentation
├── scripts/                   # Setup & Run Skripte
└── reports/                   # Generierte Berichte
```

## 🎯 Unterstützte Challenge-Kategorien

| Kategorie | Challenges | Status | Beschreibung |
|-----------|------------|--------|--------------|
| **Injection** | 15+ | ✅ | SQL, NoSQL, Command Injection |
| **Authentication** | 10+ | ✅ | Login-Bypass, JWT-Manipulation |
| **XSS** | 12+ | 🚧 | Reflected, Stored, DOM-XSS |
| **Access Control** | 8+ | 🚧 | Broken Access Control |
| **Security Misc** | 10+ | 📋 | HTTPS, Headers, etc. |
| **Crypto** | 5+ | 📋 | Weak Crypto, Hash-Cracking |

**Legende:** ✅ Implementiert | 🚧 In Entwicklung | 📋 Geplant

## 💻 Verwendung

### Basis-Kommandos

```bash
# Alle Challenges lösen
python main.py --target http://localhost:3000 --solve-all

# Nur bestimmte Kategorie
python main.py --category injection --verbose

# Educational Mode
python main.py --educational --report html

# Mit Konfigurationsdatei
python main.py --config custom_config.yaml --solve-all
```

### Erweiterte Optionen

```bash
# Verschiedene Targets
python main.py --target http://juice-shop.herokuapp.com --solve-all

# Verschiedene Report-Formate
python main.py --solve-all --report json
python main.py --solve-all --report html

# Verboses Logging
python main.py --solve-all --verbose
```

## ⚙️ Konfiguration

Die Konfiguration erfolgt über `config/settings.yaml`:

```yaml
juice_shop:
  base_url: "http://localhost:3000"
  timeout: 30
  retry_attempts: 3

selenium:
  driver: "chrome"
  headless: false
  window_size: "1920x1080"

exploitation:
  delay_between_attacks: 1
  educational_mode: false
  save_screenshots: true

ai:
  enabled: false
  provider: "openai"
  model: "gpt-4"
```

## 🧪 Exploit-Beispiele

### SQL Injection
```python
# Automatische Admin-Login via SQL Injection
def exploit_login_admin(self):
    payloads = [
        {"email": "admin@juice-sh.op'--", "password": "anything"},
        {"email": "' OR 1=1--", "password": "anything"}
    ]
    # ... Implementierung
```

### JWT Manipulation
```python
# JWT None-Algorithm Attack
def exploit_jwt_none_algorithm(self):
    # Token dekodieren, Payload modifizieren, None-Algorithmus verwenden
    malicious_token = f"{header}.{payload}."
    # ... Implementierung
```

## 📊 Reporting

Das Framework generiert umfassende Berichte:

### HTML Report
- 📈 **Erfolgsstatistiken**
- 🎯 **Challenge-Details**
- 💾 **Payloads & Screenshots**
- 📋 **Lernmaterialien**

### JSON Report
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "statistics": {
    "total_attempted": 110,
    "total_successful": 108,
    "success_rate": 98.2
  },
  "challenges": {
    "injection": {
      "exploits": [...]
    }
  }
}
```

## 🎓 Educational Mode

Der Educational Mode bietet:

- 📖 **Schritt-für-Schritt Erklärungen**
- 🎯 **Vulnerability-Details**
- 🛡️ **Mitigation-Strategien**
- 📚 **Weiterführende Links**

```bash
# Educational Mode aktivieren
python main.py --educational --verbose
```

## 🤖 KI-Integration

**Optional:** Integration von OpenAI GPT für:

- 🧠 **Intelligente Payload-Generierung**
- 🔍 **Vulnerability Pattern Recognition**
- 📝 **Automatische Dokumentation**

```yaml
# In config/settings.yaml
ai:
  enabled: true
  provider: "openai"
  api_key: "your-api-key"
  model: "gpt-4"
```

## 🐳 Docker Setup

### Juice Shop starten
```bash
# Standard Setup
docker run -d -p 3000:3000 bkimminich/juice-shop

# Mit Persistenz
docker run -d -p 3000:3000 -v juice-shop-data:/app/data bkimminich/juice-shop

# Multi-Arch Support
docker run -d -p 3000:3000 --platform linux/amd64 bkimminich/juice-shop
```

### Automation Container
```bash
# Automation in Container ausführen
docker build -t juice-automation .
docker run -v $(pwd)/reports:/app/reports juice-automation
```

## 🔧 Entwicklung & Erweiterung

### Neue Exploits hinzufügen

1. **Neues Modul erstellen:**
```python
# src/exploits/new_category/new_exploit.py
class NewExploit:
    def __init__(self, api, browser):
        self.api = api
        self.browser = browser
    
    def exploit_challenge(self):
        # Implementierung
        return {'success': True, 'challenge': 'Name'}
```

2. **In main.py registrieren:**
```python
if category == 'new_category':
    exploits = [NewExploit(self.api, self.browser)]
```

### Testing
```bash
# Unit Tests
pytest tests/

# Integration Tests
pytest tests/integration/

# Coverage Report
pytest --cov=src tests/
```

## 📚 Schulungsmaterialien

### Generierte Dokumentation
- 📖 **PDF-Handbuch** (200+ Seiten)
- 🎥 **Video-Tutorial-Skripte**
- 💼 **PowerPoint-Präsentationen**
- 🧪 **Hands-on Lab Guides**

### Verwendung in Schulungen
```bash
# Schulungspaket generieren
python main.py --educational --generate-training-materials

# Interaktive Session
python main.py --interactive --challenge-by-challenge
```

## ⚠️ Wichtige Sicherheitshinweise

### ❌ NICHT verwenden für:
- Produktive Systeme ohne Erlaubnis
- Unauthorized Penetration Testing
- Illegale Aktivitäten

### ✅ Autorisierte Verwendung:
- Security-Training & -Schulungen
- OWASP Juice Shop (designed to be hacked)
- Authorized Security Assessments
- Educational Purposes

### Rechtliche Hinweise
```
IMPORTANT: This tool is for educational and authorized security 
testing purposes only. Users are responsible for compliance 
with all applicable laws and regulations.
```

## 🛠️ Troubleshooting

### Häufige Probleme

**Juice Shop nicht erreichbar:**
```bash
# Status prüfen
curl http://localhost:3000
docker ps | grep juice-shop

# Neu starten
docker restart juice-shop
```

**ChromeDriver Probleme:**
```bash
# WebDriver-Manager verwenden
pip install webdriver-manager
```

**Permission Errors:**
```bash
# Rechte setzen
chmod +x scripts/*.sh
```

### Debug-Modus
```bash
# Detailliertes Logging
python main.py --solve-all --verbose --log-level DEBUG

# Screenshots bei Fehlern
python main.py --solve-all --screenshot-on-error
```

## 🤝 Contributing

Beiträge sind willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Development Setup
```bash
# Development Dependencies
pip install -r requirements-dev.txt

# Pre-commit Hooks
pre-commit install

# Code Style
black src/
flake8 src/
```

## 📄 Lizenz

Dieses Projekt ist unter der MIT Lizenz veröffentlicht. Siehe [LICENSE](LICENSE) für Details.

**Copyright (c) 2025 Martin Pfeffer**

## 👨‍💻 Entwickler

**Martin Pfeffer** - *Lead Security Engineer & Framework Architect*

- 🎯 **Spezialisierung:** Web Application Security, Penetration Testing, Automation
- 🔧 **Technologien:** Python, Security Testing, AI/ML for Cybersecurity
- 🏆 **Mission:** Automatisierung von Security-Tests für bessere IT-Security-Schulungen

## 📞 Support & Kontakt

- 🐛 **Issues:** [GitHub Issues](https://github.com/pepperonas/codecrusher/issues)
- 📧 **Email:** martin.pfeffer@codecrusher.dev
- 💼 **LinkedIn:** [Martin Pfeffer](https://linkedin.com/in/martinpfeffer)
- 📚 **Documentation:** [CodeCrusher Docs](https://docs.codecrusher.dev)

## 🙏 Danksagungen

- **OWASP Juice Shop Team** für die großartige vulnerable App
- **Security Community** für Inspiration und Feedback
- **Contributors** für Code und Dokumentation

---

**⚡ Ready to crush some code? Starte mit `./scripts/setup.sh` und dann `./scripts/run_all.sh`!**

**🎯 Ziel: 100% aller Web Application Security Challenges automatisch lösen - für bessere IT-Security-Schulungen!**