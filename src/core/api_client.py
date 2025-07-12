import requests
import json
import logging
from typing import Dict, Optional, Any, List
from urllib.parse import urljoin
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class JuiceShopAPI:
    """
    API Client für OWASP Juice Shop REST API Interaktionen
    """
    
    def __init__(self, base_url: str, timeout: int = 30, verify_ssl: bool = False):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = self._create_session()
        self.logger = logging.getLogger(__name__)
        self.auth_token = None
        self.user_id = None
        
    def _create_session(self) -> requests.Session:
        """Erstellt eine Session mit Retry-Strategie"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.verify = self.verify_ssl
        return session
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Führt HTTP Request aus mit Error Handling"""
        url = urljoin(self.base_url, endpoint)
        
        # Auth Token hinzufügen falls vorhanden
        if self.auth_token and 'headers' in kwargs:
            kwargs['headers']['Authorization'] = f'Bearer {self.auth_token}'
        elif self.auth_token:
            kwargs['headers'] = {'Authorization': f'Bearer {self.auth_token}'}
            
        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        
        try:
            self.logger.debug(f"{method} {url}")
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
            
    # Authentication endpoints
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Authentifizierung mit Email und Passwort"""
        data = {'email': email, 'password': password}
        response = self._make_request('POST', '/rest/user/login', json=data)
        result = response.json()
        
        if 'authentication' in result:
            self.auth_token = result['authentication']['token']
            self.user_id = result['authentication']['uId']
            self.logger.info(f"Login successful for user: {email}")
            
        return result
        
    def register(self, email: str, password: str, security_answer: str = "test", 
                 security_question_id: int = 1) -> Dict[str, Any]:
        """Registriert neuen Benutzer"""
        data = {
            'email': email,
            'password': password,
            'passwordRepeat': password,
            'securityQuestion': {
                'id': security_question_id,
                'answer': security_answer
            }
        }
        response = self._make_request('POST', '/api/Users/', json=data)
        return response.json()
        
    def whoami(self) -> Dict[str, Any]:
        """Gibt aktuelle Benutzerinformationen zurück"""
        response = self._make_request('GET', '/rest/user/whoami')
        return response.json()
        
    # Product endpoints
    def get_products(self, search: str = "") -> Dict[str, Any]:
        """Holt Produktliste mit optionaler Suche"""
        params = {'q': search} if search else {}
        response = self._make_request('GET', '/rest/products/search', params=params)
        return response.json()
        
    def get_product(self, product_id: int) -> Dict[str, Any]:
        """Holt einzelnes Produkt"""
        response = self._make_request('GET', f'/api/Products/{product_id}')
        return response.json()
        
    # Basket endpoints
    def get_basket(self, bid: int) -> Dict[str, Any]:
        """Holt Warenkorb"""
        response = self._make_request('GET', f'/rest/basket/{bid}')
        return response.json()
        
    def add_to_basket(self, product_id: int, quantity: int = 1, basket_id: Optional[int] = None) -> Dict[str, Any]:
        """Fügt Produkt zum Warenkorb hinzu"""
        data = {
            'ProductId': product_id,
            'BasketId': basket_id or self.user_id,
            'quantity': quantity
        }
        response = self._make_request('POST', '/api/BasketItems/', json=data)
        return response.json()
        
    # Feedback endpoints
    def submit_feedback(self, comment: str, rating: int = 5, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Sendet Feedback"""
        data = {
            'UserId': user_id or self.user_id,
            'comment': comment,
            'rating': rating
        }
        # CAPTCHA muss möglicherweise umgangen werden
        captcha = self.get_captcha()
        if captcha:
            data['captcha'] = captcha['answer']
            data['captchaId'] = captcha['captchaId']
            
        response = self._make_request('POST', '/api/Feedbacks/', json=data)
        return response.json()
        
    def get_feedbacks(self) -> Dict[str, Any]:
        """Holt alle Feedbacks"""
        response = self._make_request('GET', '/api/Feedbacks/')
        return response.json()
        
    # Challenge endpoints
    def get_challenges(self) -> Dict[str, Any]:
        """Holt alle Challenges"""
        response = self._make_request('GET', '/api/Challenges/')
        return response.json()
        
    def get_challenge_status(self) -> Dict[str, Any]:
        """Holt Challenge-Status"""
        response = self._make_request('GET', '/api/Challenges/?sort=name')
        challenges = response.json()
        
        solved = [c for c in challenges['data'] if c.get('solved')]
        unsolved = [c for c in challenges['data'] if not c.get('solved')]
        
        return {
            'total': len(challenges['data']),
            'solved': len(solved),
            'unsolved': len(unsolved),
            'challenges': challenges['data']
        }
        
    # Security Questions
    def get_security_questions(self) -> Dict[str, Any]:
        """Holt Sicherheitsfragen"""
        response = self._make_request('GET', '/api/SecurityQuestions/')
        return response.json()
        
    # CAPTCHA
    def get_captcha(self) -> Dict[str, Any]:
        """Holt CAPTCHA für Formulare"""
        response = self._make_request('GET', '/rest/captcha/')
        return response.json()
        
    # File endpoints
    def upload_file(self, file_path: str, field_name: str = 'file') -> Dict[str, Any]:
        """Lädt Datei hoch"""
        with open(file_path, 'rb') as f:
            files = {field_name: f}
            response = self._make_request('POST', '/file-upload', files=files)
            return response.json()
            
    # Admin endpoints
    def get_users(self) -> Dict[str, Any]:
        """Holt alle Benutzer (benötigt Admin-Rechte)"""
        response = self._make_request('GET', '/api/Users/')
        return response.json()
        
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Löscht Benutzer (benötigt Admin-Rechte)"""
        response = self._make_request('DELETE', f'/api/Users/{user_id}')
        return response.json()
        
    # Utility methods
    def check_connection(self) -> bool:
        """Überprüft Verbindung zum Juice Shop"""
        try:
            response = self._make_request('GET', '/')
            return response.status_code == 200
        except:
            return False
            
    def get_score_board(self) -> Optional[str]:
        """Versucht Score Board zu finden"""
        # Score Board ist versteckt, verschiedene Methoden zum Finden
        possible_paths = [
            '/score-board',
            '/scoreboard',
            '/score-board.html',
            '/#/score-board',
            '/api/Challenges/'
        ]
        
        for path in possible_paths:
            try:
                response = self._make_request('GET', path)
                if response.status_code == 200:
                    return f"{self.base_url}{path}"
            except:
                continue
                
        return None
        
    def close(self):
        """Schließt Session"""
        self.session.close()