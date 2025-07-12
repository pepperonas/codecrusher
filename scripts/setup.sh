#!/bin/bash

# CodeCrusher Web Security Framework Setup Script
# Installiert alle Abhängigkeiten und bereitet das System vor

set -e

echo "💥 CodeCrusher - Web Security Framework Setup"
echo "============================================="

# Prüfe Python Version
echo "🔍 Checking Python version..."
python3 --version || {
    echo "❌ Python 3 ist nicht installiert. Bitte installieren Sie Python 3.8 oder höher."
    exit 1
}

# Erstelle virtuelle Umgebung
echo "🐍 Creating virtual environment..."
python3 -m venv venv

# Aktiviere virtuelle Umgebung
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Installiere Requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Erstelle notwendige Verzeichnisse
echo "📁 Creating directories..."
mkdir -p logs reports screenshots sessions

# Prüfe Browser-Driver
echo "🌐 Checking browser drivers..."

# ChromeDriver Check
if command -v chromedriver &> /dev/null; then
    echo "✅ ChromeDriver found: $(chromedriver --version)"
else
    echo "⚠️  ChromeDriver not found. Installing via webdriver-manager..."
    pip install webdriver-manager
fi

# Docker Check für Juice Shop
echo "🐳 Checking Docker for Juice Shop..."
if command -v docker &> /dev/null; then
    echo "✅ Docker found: $(docker --version)"
    
    # Prüfe ob Juice Shop Container läuft
    if docker ps | grep -q "bkimminich/juice-shop"; then
        echo "✅ Juice Shop container is already running"
    else
        echo "🚀 Starting OWASP Juice Shop container..."
        docker run -d -p 3000:3000 --name juice-shop bkimminich/juice-shop
        echo "✅ Juice Shop started at http://localhost:3000"
        
        # Warte bis Juice Shop bereit ist
        echo "⏳ Waiting for Juice Shop to be ready..."
        for i in {1..30}; do
            if curl -s http://localhost:3000 > /dev/null 2>&1; then
                echo "✅ Juice Shop is ready!"
                break
            fi
            echo "   Waiting... ($i/30)"
            sleep 2
        done
    fi
else
    echo "⚠️  Docker not found. You'll need to start Juice Shop manually:"
    echo "   npm install -g juice-shop"
    echo "   juice-shop"
    echo "   Or download from: https://github.com/juice-shop/juice-shop"
fi

# Konfiguration vorbereiten
echo "⚙️  Preparing configuration..."
if [ ! -f "config/settings.yaml" ]; then
    echo "❌ Configuration file not found. Please ensure config/settings.yaml exists."
    exit 1
fi

# Test Setup
echo "🧪 Testing setup..."
cd src
python3 -c "
import sys
sys.path.append('.')
from core.api_client import JuiceShopAPI
try:
    api = JuiceShopAPI('http://localhost:3000')
    if api.check_connection():
        print('✅ Connection to Juice Shop successful!')
    else:
        print('❌ Cannot connect to Juice Shop. Please check if it is running.')
        sys.exit(1)
except Exception as e:
    print(f'❌ Setup test failed: {e}')
    sys.exit(1)
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run automation: cd src && python main.py --target http://localhost:3000 --educational"
echo "   3. View results in reports/ directory"
echo ""
echo "🚨 WICHTIG: Diese Tools nur für autorisierte Tests verwenden!"
echo ""
echo "📚 Für Hilfe: python main.py --help"