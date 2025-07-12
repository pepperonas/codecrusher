import json
import pickle
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import jwt


class SessionManager:
    """
    Verwaltet Sessions, Cookies und Tokens für Juice Shop
    """
    
    def __init__(self, session_dir: str = "sessions"):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.current_session = {
            'cookies': {},
            'tokens': {},
            'users': {},
            'metadata': {}
        }
        
    def save_session(self, name: str) -> None:
        """Speichert aktuelle Session"""
        session_file = self.session_dir / f"{name}.json"
        self.current_session['metadata']['saved_at'] = datetime.now().isoformat()
        
        with open(session_file, 'w') as f:
            json.dump(self.current_session, f, indent=2)
        self.logger.info(f"Session saved: {session_file}")
        
    def load_session(self, name: str) -> Dict[str, Any]:
        """Lädt gespeicherte Session"""
        session_file = self.session_dir / f"{name}.json"
        
        if not session_file.exists():
            self.logger.error(f"Session not found: {session_file}")
            return {}
            
        with open(session_file, 'r') as f:
            self.current_session = json.load(f)
        self.logger.info(f"Session loaded: {session_file}")
        return self.current_session
        
    def add_user(self, email: str, password: str, user_id: Optional[int] = None, 
                 token: Optional[str] = None) -> None:
        """Fügt Benutzer zur Session hinzu"""
        self.current_session['users'][email] = {
            'password': password,
            'user_id': user_id,
            'token': token,
            'created_at': datetime.now().isoformat()
        }
        
        if token:
            self.add_token(email, token)
            
    def add_token(self, identifier: str, token: str) -> None:
        """Fügt Token zur Session hinzu"""
        # Versuche Token zu dekodieren für Metadaten
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp = decoded.get('exp')
            expires_at = datetime.fromtimestamp(exp).isoformat() if exp else None
        except:
            expires_at = None
            
        self.current_session['tokens'][identifier] = {
            'token': token,
            'added_at': datetime.now().isoformat(),
            'expires_at': expires_at
        }
        
    def get_token(self, identifier: str) -> Optional[str]:
        """Holt Token aus Session"""
        token_data = self.current_session['tokens'].get(identifier)
        if not token_data:
            return None
            
        # Prüfe ob Token abgelaufen
        if token_data.get('expires_at'):
            expires_at = datetime.fromisoformat(token_data['expires_at'])
            if datetime.now() > expires_at:
                self.logger.warning(f"Token expired for {identifier}")
                return None
                
        return token_data['token']
        
    def add_cookie(self, name: str, value: str, domain: str = None, 
                   path: str = "/", expires: Optional[datetime] = None) -> None:
        """Fügt Cookie zur Session hinzu"""
        self.current_session['cookies'][name] = {
            'value': value,
            'domain': domain,
            'path': path,
            'expires': expires.isoformat() if expires else None,
            'added_at': datetime.now().isoformat()
        }
        
    def get_cookies(self) -> Dict[str, Any]:
        """Gibt alle Cookies zurück"""
        return self.current_session['cookies']
        
    def get_cookie(self, name: str) -> Optional[str]:
        """Holt einzelnen Cookie"""
        cookie = self.current_session['cookies'].get(name)
        return cookie['value'] if cookie else None
        
    def clear_session(self) -> None:
        """Löscht aktuelle Session"""
        self.current_session = {
            'cookies': {},
            'tokens': {},
            'users': {},
            'metadata': {}
        }
        
    def list_sessions(self) -> list:
        """Listet alle gespeicherten Sessions auf"""
        return [f.stem for f in self.session_dir.glob("*.json")]
        
    def delete_session(self, name: str) -> bool:
        """Löscht gespeicherte Session"""
        session_file = self.session_dir / f"{name}.json"
        if session_file.exists():
            session_file.unlink()
            self.logger.info(f"Session deleted: {name}")
            return True
        return False
        
    def export_for_selenium(self) -> list:
        """Exportiert Cookies für Selenium WebDriver"""
        selenium_cookies = []
        for name, cookie_data in self.current_session['cookies'].items():
            selenium_cookie = {
                'name': name,
                'value': cookie_data['value'],
                'domain': cookie_data.get('domain', 'localhost'),
                'path': cookie_data.get('path', '/'),
                'secure': False,
                'httpOnly': False
            }
            if cookie_data.get('expires'):
                expires = datetime.fromisoformat(cookie_data['expires'])
                selenium_cookie['expiry'] = int(expires.timestamp())
            selenium_cookies.append(selenium_cookie)
        return selenium_cookies
        
    def import_from_selenium(self, selenium_cookies: list) -> None:
        """Importiert Cookies von Selenium WebDriver"""
        for cookie in selenium_cookies:
            expires = None
            if 'expiry' in cookie:
                expires = datetime.fromtimestamp(cookie['expiry'])
            
            self.add_cookie(
                name=cookie['name'],
                value=cookie['value'],
                domain=cookie.get('domain'),
                path=cookie.get('path', '/'),
                expires=expires
            )
            
    def get_admin_credentials(self) -> Optional[Dict[str, str]]:
        """Versucht Admin-Credentials zu finden"""
        # Standard Admin Credentials für Juice Shop
        default_admins = [
            {'email': 'admin@juice-sh.op', 'password': 'admin123'},
            {'email': 'admin@juice-sh.op', 'password': 'admin'},
            {'email': 'admin@juice-sh.op', 'password': '0192023a7bbd73250516f069df18b500'},  # MD5 of admin123
        ]
        
        # Prüfe gespeicherte Users
        for email, user_data in self.current_session['users'].items():
            if 'admin' in email.lower():
                return {'email': email, 'password': user_data['password']}
                
        # Return default admin creds
        return default_admins[0]
        
    def save_exploit_result(self, challenge_name: str, payload: str, 
                           success: bool, details: Dict[str, Any] = None) -> None:
        """Speichert Exploit-Ergebnis"""
        if 'exploits' not in self.current_session['metadata']:
            self.current_session['metadata']['exploits'] = []
            
        exploit_data = {
            'challenge': challenge_name,
            'payload': payload,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        
        self.current_session['metadata']['exploits'].append(exploit_data)
        
    def get_exploit_history(self, challenge_name: Optional[str] = None) -> list:
        """Holt Exploit-Historie"""
        exploits = self.current_session['metadata'].get('exploits', [])
        
        if challenge_name:
            return [e for e in exploits if e['challenge'] == challenge_name]
        return exploits