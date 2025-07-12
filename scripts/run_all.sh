#!/bin/bash

# CodeCrusher - Run All Security Challenges
# Führt alle verfügbaren Security-Tests automatisch aus

set -e

# Farbdefinitionen
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "██████╗ ██╗   ██╗██╗ ██████╗███████╗    ███████╗██╗  ██╗ ██████╗ ██████╗ "
echo "██╔══██╗██║   ██║██║██╔════╝██╔════╝    ██╔════╝██║  ██║██╔═══██╗██╔══██╗"
echo "██████╔╝██║   ██║██║██║     █████╗      ███████╗███████║██║   ██║██████╔╝"
echo "██╔══██╗██║   ██║██║██║     ██╔══╝      ╚════██║██╔══██║██║   ██║██╔═══╝ "
echo "██║  ██║╚██████╔╝██║╚██████╗███████╗    ███████║██║  ██║╚██████╔╝██║     "
echo "╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝╚══════╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     "
echo "                                                                          "
echo "              🛡️  VOLLAUTOMATISIERUNG ALLER CHALLENGES  🛡️"
echo -e "${NC}"

# Parameter
TARGET_URL="${1:-http://localhost:3000}"
REPORT_FORMAT="${2:-html}"
MODE="${3:-all}"

echo -e "${YELLOW}⚙️  Konfiguration:${NC}"
echo "   🎯 Target: $TARGET_URL"
echo "   📄 Report: $REPORT_FORMAT"
echo "   🎮 Mode: $MODE"
echo ""

# Prüfe ob virtuelle Umgebung aktiv ist
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️  Aktiviere virtuelle Umgebung...${NC}"
    source ../venv/bin/activate
fi

# Prüfe Juice Shop Verbindung
echo -e "${BLUE}🔍 Teste Verbindung zu Juice Shop...${NC}"
if curl -s "$TARGET_URL" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Juice Shop erreichbar${NC}"
else
    echo -e "${RED}❌ Juice Shop nicht erreichbar. Starte Container...${NC}"
    
    # Versuche Juice Shop zu starten
    if command -v docker &> /dev/null; then
        docker run -d -p 3000:3000 --name juice-shop-auto bkimminich/juice-shop 2>/dev/null || \
        docker start juice-shop-auto 2>/dev/null || \
        echo -e "${RED}❌ Docker-Start fehlgeschlagen. Bitte manuell starten.${NC}"
        
        # Warte auf Start
        echo -e "${YELLOW}⏳ Warte auf Juice Shop...${NC}"
        for i in {1..30}; do
            if curl -s "$TARGET_URL" > /dev/null 2>&1; then
                echo -e "${GREEN}✅ Juice Shop ist bereit!${NC}"
                break
            fi
            sleep 2
        done
    fi
fi

echo ""

# Wechsle in src Verzeichnis
cd ../src

# Erstelle Session-Name
SESSION_NAME="auto_$(date +%Y%m%d_%H%M%S)"

echo -e "${BLUE}🚀 Starte Automation Framework...${NC}"
echo ""

# Führe basierend auf Modus aus
case $MODE in
    "educational")
        echo -e "${YELLOW}📚 Educational Mode - Mit Erklärungen${NC}"
        python main.py --target "$TARGET_URL" --educational --report "$REPORT_FORMAT" --verbose
        ;;
    "injection")
        echo -e "${YELLOW}💉 Nur Injection Attacks${NC}"
        python main.py --target "$TARGET_URL" --category injection --report "$REPORT_FORMAT" --verbose
        ;;
    "auth")
        echo -e "${YELLOW}🔐 Nur Authentication Attacks${NC}"
        python main.py --target "$TARGET_URL" --category authentication --report "$REPORT_FORMAT" --verbose
        ;;
    "fast")
        echo -e "${YELLOW}⚡ Fast Mode - Nur kritische Exploits${NC}"
        python main.py --target "$TARGET_URL" --solve-all --report "$REPORT_FORMAT"
        ;;
    *)
        echo -e "${YELLOW}🎯 Full Automation - Alle Challenges${NC}"
        python main.py --target "$TARGET_URL" --solve-all --report "$REPORT_FORMAT" --verbose
        ;;
esac

# Ergebnis auswerten
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}🎉 Automation erfolgreich abgeschlossen!${NC}"
    
    # Zeige Berichte
    echo -e "${BLUE}📊 Generierte Berichte:${NC}"
    ls -la ../reports/ | tail -5
    
    # Öffne HTML-Report falls vorhanden
    if [ "$REPORT_FORMAT" == "html" ] && [ -f "../reports/"*".html" ]; then
        LATEST_REPORT=$(ls -t ../reports/*.html | head -1)
        echo -e "${GREEN}🌐 Öffne Bericht: $LATEST_REPORT${NC}"
        
        # Versuche Browser zu öffnen
        if command -v open &> /dev/null; then
            open "$LATEST_REPORT"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "$LATEST_REPORT"
        elif command -v firefox &> /dev/null; then
            firefox "$LATEST_REPORT" &
        else
            echo "   Öffne manuell: $LATEST_REPORT"
        fi
    fi
    
else
    echo -e "${RED}❌ Automation mit Fehlern beendet (Exit Code: $EXIT_CODE)${NC}"
fi

echo ""
echo -e "${BLUE}📋 Nützliche Befehle:${NC}"
echo "   📄 Logs anzeigen: tail -f ../logs/*.log"
echo "   🔄 Erneut ausführen: $0 $TARGET_URL $REPORT_FORMAT $MODE"
echo "   🧹 Cleanup: docker stop juice-shop-auto"
echo ""

echo -e "${RED}⚠️  WICHTIGER HINWEIS:${NC}"
echo -e "${RED}   Diese Tools nur für autorisierte Security-Tests verwenden!${NC}"
echo -e "${RED}   Niemals gegen produktive Systeme ohne explizite Erlaubnis!${NC}"
echo ""

exit $EXIT_CODE