#!/usr/bin/env python3
"""
CodeCrusher - Web Application Security Testing Framework
Vollautomatisierte Lösung aller Web Security Challenges

Author: Martin Pfeffer (c) 2025
License: MIT

Usage:
    python main.py --target http://localhost:3000 --solve-all
    python main.py --category injection --verbose
    python main.py --educational --report
"""

import argparse
import logging
import time
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from core.api_client import JuiceShopAPI
from core.session_manager import SessionManager
from core.browser_automation import BrowserAutomation

from exploits.injection.sql_injection import SQLInjectionExploits
from exploits.injection.nosql_injection import NoSQLInjectionExploits
from exploits.injection.command_injection import CommandInjectionExploits
from exploits.authentication.auth_bypass import AuthenticationBypassExploits
from exploits.authentication.token_manipulation import TokenManipulationExploits


class CodeCrusher:
    """
    Hauptklasse für das CodeCrusher Web Security Testing Framework
    
    Author: Martin Pfeffer (c) 2025
    """
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        
        # Core components
        self.api = None
        self.browser = None
        self.session_manager = SessionManager()
        
        # Results storage
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'config': self.config,
            'challenges': {},
            'statistics': {
                'total_attempted': 0,
                'total_successful': 0,
                'total_failed': 0,
                'categories': {}
            }
        }
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Lädt Konfiguration"""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
            
    def _setup_logging(self) -> logging.Logger:
        """Setup Logging"""
        log_config = self.config.get('logging', {})
        
        # Create logs directory
        Path(log_config.get('file', 'logs/automation.log')).parent.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_config.get('level', 'INFO')),
            format=log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            handlers=[
                logging.FileHandler(log_config.get('file', 'logs/automation.log')),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger(__name__)
        logger.info("CodeCrusher Web Security Framework initialized - Martin Pfeffer (c) 2025")
        return logger
        
    def initialize(self, target_url: str) -> None:
        """Initialisiert API und Browser"""
        self.logger.info(f"Initializing connection to: {target_url}")
        
        # Initialize API client
        juice_config = self.config.get('juice_shop', {})
        self.api = JuiceShopAPI(
            base_url=target_url,
            timeout=juice_config.get('timeout', 30),
            verify_ssl=self.config.get('security', {}).get('verify_ssl', False)
        )
        
        # Test connection
        if not self.api.check_connection():
            raise ConnectionError(f"Cannot connect to target application at {target_url}")
            
        # Initialize browser if needed
        selenium_config = self.config.get('selenium', {})
        if selenium_config.get('enabled', True):
            self.browser = BrowserAutomation(
                driver_type=selenium_config.get('driver', 'chrome'),
                headless=selenium_config.get('headless', False),
                window_size=selenium_config.get('window_size', '1920x1080')
            )
            self.browser.start(target_url)
            
        self.logger.info("Initialization completed successfully")
        
    def run_category(self, category: str) -> Dict[str, Any]:
        """Führt alle Exploits einer Kategorie aus"""
        self.logger.info(f"Running category: {category}")
        
        category_results = {
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'exploits': []
        }
        
        if category == 'injection':
            exploits = [
                SQLInjectionExploits(self.api, self.browser),
                NoSQLInjectionExploits(self.api, self.browser),
                CommandInjectionExploits(self.api, self.browser)
            ]
        elif category == 'authentication':
            exploits = [
                AuthenticationBypassExploits(self.api, self.browser),
                TokenManipulationExploits(self.api, self.browser)
            ]
        else:
            self.logger.warning(f"Category not implemented: {category}")
            return category_results
            
        # Run all exploits in category
        for exploit_class in exploits:
            try:
                self.logger.info(f"Running: {exploit_class.__class__.__name__}")
                exploit_results = exploit_class.run_all()
                category_results['exploits'].extend(exploit_results)
                
                # Update statistics
                for result in exploit_results:
                    self.results['statistics']['total_attempted'] += 1
                    if result.get('success', False):
                        self.results['statistics']['total_successful'] += 1
                    else:
                        self.results['statistics']['total_failed'] += 1
                        
            except Exception as e:
                self.logger.error(f"Exploit class failed: {exploit_class.__class__.__name__}: {e}")
                category_results['exploits'].append({
                    'success': False,
                    'error': str(e),
                    'exploit_class': exploit_class.__class__.__name__
                })
                
        return category_results
        
    def solve_all_challenges(self) -> Dict[str, Any]:
        """Löst alle verfügbaren Challenges"""
        self.logger.info("Starting to solve all challenges")
        
        categories = [
            'injection',
            'authentication',
            # 'xss',
            # 'access_control',
            # 'security_misc',
            # Add more categories as implemented
        ]
        
        for category in categories:
            if category in self.config.get('challenges', {}).get('categories_to_skip', []):
                self.logger.info(f"Skipping category: {category}")
                continue
                
            try:
                category_results = self.run_category(category)
                self.results['challenges'][category] = category_results
                
                # Delay between categories
                delay = self.config.get('exploitation', {}).get('delay_between_attacks', 1)
                time.sleep(delay)
                
            except Exception as e:
                self.logger.error(f"Category failed: {category}: {e}")
                
        return self.results
        
    def run_educational_mode(self) -> None:
        """Führt Educational Mode aus mit Erklärungen"""
        self.logger.info("Running in educational mode")
        
        print("\n" + "="*80)
        print("CODECRUSHER - WEB SECURITY TESTING FRAMEWORK")
        print("Educational Mode by Martin Pfeffer (c) 2025")
        print("="*80)
        
        print(f"""
CodeCrusher demonstrates various web application security vulnerabilities
and provides automated exploitation techniques for educational purposes.

Target: {self.api.base_url}
Configuration: {self.config.get('exploitation', {})}

WICHTIG: Diese Tools sind nur für autorisierte Security-Tests und Bildungszwecke
zu verwenden. Niemals gegen Systeme einsetzen, für die keine ausdrückliche
Erlaubnis vorliegt.

Kategorien, die getestet werden:
""")
        
        categories = {
            'injection': 'SQL, NoSQL und Command Injection Angriffe',
            'authentication': 'Authentifizierung-Bypass und Token-Manipulation',
            'xss': 'Cross-Site Scripting Angriffe',
            'access_control': 'Broken Access Control Vulnerabilities'
        }
        
        for cat, desc in categories.items():
            print(f"  - {cat}: {desc}")
            
        print("\nDrücke Enter um fortzufahren oder Ctrl+C zum Abbrechen...")
        input()
        
        # Run with detailed explanations
        self.solve_all_challenges()
        
    def generate_report(self, output_format: str = 'html') -> str:
        """Generiert Bericht"""
        self.logger.info(f"Generating {output_format} report")
        
        # Create reports directory
        reports_dir = Path(self.config.get('reporting', {}).get('output_dir', 'reports'))
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format == 'json':
            report_file = reports_dir / f"juice_shop_report_{timestamp}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
                
        elif output_format == 'html':
            report_file = reports_dir / f"juice_shop_report_{timestamp}.html"
            self._generate_html_report(report_file)
            
        self.logger.info(f"Report generated: {report_file}")
        return str(report_file)
        
    def _generate_html_report(self, output_file: Path) -> None:
        """Generiert HTML-Bericht"""
        html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeCrusher Security Testing Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background-color: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .success {{ color: green; font-weight: bold; }}
        .failure {{ color: red; font-weight: bold; }}
        .category {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .exploit {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-radius: 3px; }}
        .statistics {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 3px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>💥 CodeCrusher Security Testing Report</h1>
        <p><strong>Author:</strong> Martin Pfeffer (c) 2025</p>
        <p><strong>Generiert:</strong> {self.results['timestamp']}</p>
        <p><strong>Target:</strong> {self.api.base_url}</p>
    </div>
    
    <div class="statistics">
        <h2>📊 Statistiken</h2>
        <p><strong>Gesamt versucht:</strong> {self.results['statistics']['total_attempted']}</p>
        <p><strong>Erfolgreich:</strong> <span class="success">{self.results['statistics']['total_successful']}</span></p>
        <p><strong>Fehlgeschlagen:</strong> <span class="failure">{self.results['statistics']['total_failed']}</span></p>
        <p><strong>Erfolgsrate:</strong> {(self.results['statistics']['total_successful'] / max(1, self.results['statistics']['total_attempted']) * 100):.1f}%</p>
    </div>
"""
        
        # Add category results
        for category_name, category_data in self.results['challenges'].items():
            html_content += f"""
    <div class="category">
        <h2>🎯 {category_name.title()}</h2>
        <p><strong>Ausgeführt:</strong> {category_data['timestamp']}</p>
"""
            
            for exploit in category_data.get('exploits', []):
                status_class = 'success' if exploit.get('success', False) else 'failure'
                status_text = '✅ Erfolgreich' if exploit.get('success', False) else '❌ Fehlgeschlagen'
                
                html_content += f"""
        <div class="exploit">
            <h3 class="{status_class}">{exploit.get('challenge', 'Unknown')} - {status_text}</h3>
"""
                
                if exploit.get('payload'):
                    html_content += f"<p><strong>Payload:</strong> <code>{exploit['payload']}</code></p>"
                    
                if exploit.get('error'):
                    html_content += f"<p><strong>Fehler:</strong> {exploit['error']}</p>"
                    
                html_content += "</div>"
                
            html_content += "</div>"
            
        html_content += """
    <div class="footer">
        <h2>⚠️ Wichtige Hinweise</h2>
        <ul>
            <li>Diese Tests dürfen nur auf autorisierten Systemen durchgeführt werden</li>
            <li>OWASP Juice Shop ist eine absichtlich verwundbare Anwendung für Bildungszwecke</li>
            <li>Niemals diese Techniken gegen produktive Systeme ohne explizite Erlaubnis anwenden</li>
            <li>Für Fragen oder Schulungen: Kontaktieren Sie Ihr Security-Team</li>
        </ul>
    </div>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
    def cleanup(self) -> None:
        """Aufräumen"""
        self.logger.info("Cleaning up resources")
        
        if self.browser:
            self.browser.close()
            
        if self.api:
            self.api.close()


def main():
    """Hauptfunktion"""
    parser = argparse.ArgumentParser(
        description="CodeCrusher - Web Application Security Testing Framework by Martin Pfeffer (c) 2025",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python main.py --target http://localhost:3000 --solve-all
  python main.py --category injection --verbose --educational
  python main.py --target http://vulnerable-app.com --report html
        """
    )
    
    parser.add_argument('--target', '-t', 
                       default='http://localhost:3000',
                       help='Target application URL (default: http://localhost:3000)')
    
    parser.add_argument('--solve-all', '-a',
                       action='store_true',
                       help='Löse alle verfügbaren Challenges')
    
    parser.add_argument('--category', '-c',
                       choices=['injection', 'authentication', 'xss', 'access_control'],
                       help='Führe nur spezifische Kategorie aus')
    
    parser.add_argument('--educational', '-e',
                       action='store_true',
                       help='Educational Mode mit Erklärungen')
    
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Verbose Output')
    
    parser.add_argument('--report', '-r',
                       choices=['html', 'json'],
                       help='Generiere Bericht im angegebenen Format')
    
    parser.add_argument('--config', 
                       default='config/settings.yaml',
                       help='Pfad zur Konfigurationsdatei')
    
    args = parser.parse_args()
    
    try:
        # Initialize CodeCrusher framework
        automation = CodeCrusher(args.config)
        automation.initialize(args.target)
        
        # Run based on arguments
        if args.educational:
            automation.run_educational_mode()
        elif args.solve_all:
            automation.solve_all_challenges()
        elif args.category:
            automation.run_category(args.category)
        else:
            print("Kein Modus angegeben. Verwende --help für Hilfe.")
            return
            
        # Generate report if requested
        if args.report:
            report_file = automation.generate_report(args.report)
            print(f"📄 Bericht generiert: {report_file}")
            
        # Print summary
        stats = automation.results['statistics']
        print(f"""
🎯 Zusammenfassung:
   Gesamt versucht: {stats['total_attempted']}
   Erfolgreich: {stats['total_successful']}
   Fehlgeschlagen: {stats['total_failed']}
   Erfolgsrate: {(stats['total_successful'] / max(1, stats['total_attempted']) * 100):.1f}%
""")
        
    except KeyboardInterrupt:
        print("\n⚠️ Abgebrochen durch Benutzer")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        logging.error(f"Application error: {e}", exc_info=True)
    finally:
        if 'automation' in locals():
            automation.cleanup()


if __name__ == "__main__":
    main()