import logging
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class BrowserAutomation:
    """
    Browser Automation für Juice Shop mit Selenium WebDriver
    """
    
    def __init__(self, driver_type: str = "chrome", headless: bool = False, 
                 window_size: str = "1920x1080", screenshots_dir: str = "screenshots"):
        self.driver_type = driver_type.lower()
        self.headless = headless
        self.window_size = window_size
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(exist_ok=True)
        self.driver = None
        self.wait = None
        self.logger = logging.getLogger(__name__)
        
    def start(self, base_url: str = None) -> None:
        """Startet Browser"""
        self.driver = self._create_driver()
        self.wait = WebDriverWait(self.driver, 10)
        
        if base_url:
            self.navigate(base_url)
            self.handle_welcome_banner()
            
    def _create_driver(self) -> webdriver.Remote:
        """Erstellt WebDriver basierend auf Konfiguration"""
        width, height = self.window_size.split('x')
        
        if self.driver_type == "chrome":
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument(f"--window-size={width},{height}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            return webdriver.Chrome(options=options)
            
        elif self.driver_type == "firefox":
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument(f"--width={width}")
            options.add_argument(f"--height={height}")
            return webdriver.Firefox(options=options)
            
        elif self.driver_type == "edge":
            options = EdgeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument(f"--window-size={width},{height}")
            return webdriver.Edge(options=options)
            
        else:
            raise ValueError(f"Unsupported driver type: {self.driver_type}")
            
    def navigate(self, url: str) -> None:
        """Navigiert zu URL"""
        self.logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        time.sleep(1)  # Warte auf initiales Laden
        
    def handle_welcome_banner(self) -> None:
        """Schließt Welcome Banner falls vorhanden"""
        try:
            # Warte auf Banner und schließe es
            dismiss_button = self.wait_for_element(
                By.CSS_SELECTOR, 
                "button[aria-label='Close Welcome Banner']", 
                timeout=5
            )
            if dismiss_button:
                dismiss_button.click()
                self.logger.info("Welcome banner dismissed")
                
            # Cookie consent
            cookie_button = self.find_element(By.CSS_SELECTOR, "a.cc-dismiss")
            if cookie_button:
                cookie_button.click()
                self.logger.info("Cookie consent accepted")
        except:
            pass
            
    def wait_for_element(self, by: By, value: str, timeout: int = 10) -> Optional[Any]:
        """Wartet auf Element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"Element not found: {by}={value}")
            return None
            
    def wait_for_clickable(self, by: By, value: str, timeout: int = 10) -> Optional[Any]:
        """Wartet bis Element klickbar ist"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"Element not clickable: {by}={value}")
            return None
            
    def find_element(self, by: By, value: str) -> Optional[Any]:
        """Findet Element ohne zu warten"""
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return None
            
    def find_elements(self, by: By, value: str) -> List[Any]:
        """Findet alle Elemente"""
        return self.driver.find_elements(by, value)
        
    def click(self, element: Any) -> bool:
        """Klickt auf Element mit Fehlerbehandlung"""
        try:
            # Scroll zu Element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Versuche normalen Click
            element.click()
            return True
        except:
            try:
                # Fallback: JavaScript Click
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except Exception as e:
                self.logger.error(f"Failed to click element: {e}")
                return False
                
    def type_text(self, element: Any, text: str, clear: bool = True) -> None:
        """Tippt Text in Element"""
        if clear:
            element.clear()
        element.send_keys(text)
        
    def execute_js(self, script: str, *args) -> Any:
        """Führt JavaScript aus"""
        return self.driver.execute_script(script, *args)
        
    def get_cookies(self) -> List[Dict[str, Any]]:
        """Holt alle Cookies"""
        return self.driver.get_cookies()
        
    def add_cookie(self, cookie: Dict[str, Any]) -> None:
        """Fügt Cookie hinzu"""
        self.driver.add_cookie(cookie)
        
    def delete_all_cookies(self) -> None:
        """Löscht alle Cookies"""
        self.driver.delete_all_cookies()
        
    def take_screenshot(self, name: str) -> str:
        """Macht Screenshot"""
        filename = self.screenshots_dir / f"{name}_{int(time.time())}.png"
        self.driver.save_screenshot(str(filename))
        self.logger.info(f"Screenshot saved: {filename}")
        return str(filename)
        
    def get_page_source(self) -> str:
        """Gibt Seitenquelltext zurück"""
        return self.driver.page_source
        
    def get_current_url(self) -> str:
        """Gibt aktuelle URL zurück"""
        return self.driver.current_url
        
    def refresh(self) -> None:
        """Lädt Seite neu"""
        self.driver.refresh()
        
    def back(self) -> None:
        """Navigiert zurück"""
        self.driver.back()
        
    def forward(self) -> None:
        """Navigiert vorwärts"""
        self.driver.forward()
        
    # Juice Shop spezifische Methoden
    def login(self, email: str, password: str) -> bool:
        """Login über UI"""
        try:
            # Navigate to login
            self.navigate_to_login()
            
            # Fill form
            email_input = self.wait_for_element(By.ID, "email")
            password_input = self.wait_for_element(By.ID, "password")
            
            self.type_text(email_input, email)
            self.type_text(password_input, password)
            
            # Submit
            login_button = self.wait_for_clickable(By.ID, "loginButton")
            self.click(login_button)
            
            # Check success
            time.sleep(2)
            if "Your Basket" in self.get_page_source():
                self.logger.info(f"Login successful: {email}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False
            
    def navigate_to_login(self) -> None:
        """Navigiert zur Login-Seite"""
        # Click Account menu
        account_button = self.wait_for_clickable(By.ID, "navbarAccount")
        self.click(account_button)
        
        # Click Login
        login_link = self.wait_for_clickable(By.ID, "navbarLoginButton")
        self.click(login_link)
        time.sleep(1)
        
    def navigate_to_registration(self) -> None:
        """Navigiert zur Registrierung"""
        self.navigate_to_login()
        
        # Click "Not yet a customer?"
        register_link = self.wait_for_clickable(By.CSS_SELECTOR, "a[href='#/register']")
        self.click(register_link)
        time.sleep(1)
        
    def search_products(self, query: str) -> None:
        """Sucht nach Produkten"""
        # Click search icon
        search_icon = self.wait_for_clickable(By.CSS_SELECTOR, "mat-icon[aria-label='Search']")
        self.click(search_icon)
        
        # Type search
        search_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='search']")
        self.type_text(search_input, query)
        search_input.send_keys(Keys.ENTER)
        time.sleep(1)
        
    def add_product_to_basket(self, product_index: int = 0) -> bool:
        """Fügt Produkt zum Warenkorb hinzu"""
        try:
            products = self.find_elements(By.CSS_SELECTOR, "mat-card")
            if product_index < len(products):
                add_button = products[product_index].find_element(
                    By.CSS_SELECTOR, "button[aria-label*='Add to Basket']"
                )
                self.click(add_button)
                time.sleep(1)
                return True
        except Exception as e:
            self.logger.error(f"Failed to add product: {e}")
        return False
        
    def navigate_to_basket(self) -> None:
        """Navigiert zum Warenkorb"""
        basket_button = self.wait_for_clickable(By.CSS_SELECTOR, "button[aria-label='Show the shopping cart']")
        self.click(basket_button)
        time.sleep(1)
        
    def bypass_client_validation(self, callback: Callable) -> Any:
        """Umgeht Client-seitige Validierung"""
        # Disable form validation
        self.execute_js("""
            document.querySelectorAll('input').forEach(input => {
                input.removeAttribute('required');
                input.removeAttribute('pattern');
                input.removeAttribute('min');
                input.removeAttribute('max');
                input.removeAttribute('minlength');
                input.removeAttribute('maxlength');
            });
            document.querySelectorAll('button').forEach(btn => {
                btn.removeAttribute('disabled');
            });
        """)
        
        # Execute callback
        return callback()
        
    def intercept_requests(self) -> None:
        """Setup für Request Interception (benötigt Selenium Wire)"""
        # Dies würde selenium-wire benötigen für vollständige Implementierung
        self.logger.warning("Request interception requires selenium-wire")
        
    def close(self) -> None:
        """Schließt Browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")