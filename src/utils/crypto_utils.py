import hashlib
import base64
import json
import hmac
import logging
from typing import Dict, List, Any, Optional, Union
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import itertools
import string


class CryptoUtils:
    """
    Kryptographie-Utilities für Juice Shop Challenges
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def hash_crack_md5(self, target_hash: str, wordlist: List[str] = None) -> Optional[str]:
        """
        MD5 Hash-Cracking
        """
        if not wordlist:
            wordlist = self.get_common_passwords()
            
        target_hash = target_hash.lower()
        
        for password in wordlist:
            md5_hash = hashlib.md5(password.encode()).hexdigest()
            if md5_hash == target_hash:
                self.logger.info(f"MD5 hash cracked: {target_hash} = {password}")
                return password
                
        # Brute force für kurze Passwörter
        for length in range(1, 6):
            for password in self._generate_bruteforce_passwords(length):
                md5_hash = hashlib.md5(password.encode()).hexdigest()
                if md5_hash == target_hash:
                    self.logger.info(f"MD5 hash brute-forced: {target_hash} = {password}")
                    return password
                    
        return None
        
    def hash_crack_sha1(self, target_hash: str, wordlist: List[str] = None) -> Optional[str]:
        """
        SHA1 Hash-Cracking
        """
        if not wordlist:
            wordlist = self.get_common_passwords()
            
        target_hash = target_hash.lower()
        
        for password in wordlist:
            sha1_hash = hashlib.sha1(password.encode()).hexdigest()
            if sha1_hash == target_hash:
                self.logger.info(f"SHA1 hash cracked: {target_hash} = {password}")
                return password
                
        return None
        
    def hash_crack_sha256(self, target_hash: str, wordlist: List[str] = None) -> Optional[str]:
        """
        SHA256 Hash-Cracking
        """
        if not wordlist:
            wordlist = self.get_common_passwords()
            
        target_hash = target_hash.lower()
        
        for password in wordlist:
            sha256_hash = hashlib.sha256(password.encode()).hexdigest()
            if sha256_hash == target_hash:
                self.logger.info(f"SHA256 hash cracked: {target_hash} = {password}")
                return password
                
        return None
        
    def crack_weak_encryption(self, ciphertext: str, algorithm: str = "auto") -> Dict[str, Any]:
        """
        Schwache Verschlüsselung knacken
        """
        results = []
        
        # Base64 Decoding
        try:
            decoded = base64.b64decode(ciphertext)
            if decoded.isprintable():
                results.append({
                    "method": "base64",
                    "plaintext": decoded.decode(),
                    "success": True
                })
        except:
            pass
            
        # ROT13
        try:
            rot13_result = self._rot13_decode(ciphertext)
            if rot13_result:
                results.append({
                    "method": "rot13",
                    "plaintext": rot13_result,
                    "success": True
                })
        except:
            pass
            
        # Caesar Cipher
        for shift in range(1, 26):
            try:
                caesar_result = self._caesar_decode(ciphertext, shift)
                if self._is_likely_plaintext(caesar_result):
                    results.append({
                        "method": f"caesar_shift_{shift}",
                        "plaintext": caesar_result,
                        "success": True
                    })
            except:
                pass
                
        # XOR mit einfachen Keys
        for key in ['key', 'password', 'secret', 'admin']:
            try:
                xor_result = self._xor_decode(ciphertext, key)
                if self._is_likely_plaintext(xor_result):
                    results.append({
                        "method": f"xor_{key}",
                        "plaintext": xor_result,
                        "success": True
                    })
            except:
                pass
                
        return {"results": results, "total_methods_tried": len(results)}
        
    def _rot13_decode(self, text: str) -> str:
        """ROT13 Dekodierung"""
        return ''.join(
            chr((ord(c) - ord('a') + 13) % 26 + ord('a')) if 'a' <= c <= 'z'
            else chr((ord(c) - ord('A') + 13) % 26 + ord('A')) if 'A' <= c <= 'Z'
            else c
            for c in text
        )
        
    def _caesar_decode(self, text: str, shift: int) -> str:
        """Caesar Cipher Dekodierung"""
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            else:
                result += char
        return result
        
    def _xor_decode(self, ciphertext: str, key: str) -> str:
        """XOR Dekodierung"""
        try:
            # Hex zu Bytes
            cipher_bytes = bytes.fromhex(ciphertext)
            key_bytes = key.encode()
            
            plaintext = ""
            for i, byte in enumerate(cipher_bytes):
                plaintext += chr(byte ^ key_bytes[i % len(key_bytes)])
                
            return plaintext
        except:
            # Fallback: Direkte XOR
            result = ""
            key_len = len(key)
            for i, char in enumerate(ciphertext):
                result += chr(ord(char) ^ ord(key[i % key_len]))
            return result
            
    def _is_likely_plaintext(self, text: str) -> bool:
        """Heuristik zur Erkennung von Klartext"""
        if not text:
            return False
            
        # Prüfe auf lesbare Zeichen
        printable_ratio = sum(1 for c in text if c.isprintable()) / len(text)
        if printable_ratio < 0.8:
            return False
            
        # Prüfe auf englische Wörter
        common_words = ['the', 'and', 'you', 'that', 'was', 'for', 'are', 'with', 'his', 'they']
        text_lower = text.lower()
        word_count = sum(1 for word in common_words if word in text_lower)
        
        return word_count > 0 or any(word in text_lower for word in ['admin', 'password', 'user', 'flag'])
        
    def weak_random_prediction(self, observed_values: List[int], count: int = 10) -> List[int]:
        """
        Vorhersage schwacher Zufallszahlen
        """
        if len(observed_values) < 2:
            return []
            
        # Linear Congruential Generator (LCG) Detection
        predictions = []
        
        # Versuche häufige LCG-Parameter
        lcg_params = [
            {"a": 1103515245, "c": 12345, "m": 2**31},  # GCC
            {"a": 214013, "c": 2531011, "m": 2**32},    # Microsoft
            {"a": 16807, "c": 0, "m": 2**31 - 1},       # Park-Miller
        ]
        
        for params in lcg_params:
            try:
                # Versuche LCG-Muster zu erkennen
                if self._test_lcg_pattern(observed_values, params):
                    # Generiere Vorhersagen
                    last_value = observed_values[-1]
                    for _ in range(count):
                        next_val = (params["a"] * last_value + params["c"]) % params["m"]
                        predictions.append(next_val)
                        last_value = next_val
                    break
            except:
                continue
                
        if not predictions:
            # Fallback: Einfache Muster
            diff = observed_values[-1] - observed_values[-2]
            for i in range(count):
                predictions.append(observed_values[-1] + diff * (i + 1))
                
        return predictions
        
    def _test_lcg_pattern(self, values: List[int], params: Dict[str, int]) -> bool:
        """Testet ob Werte einem LCG-Muster folgen"""
        if len(values) < 3:
            return False
            
        for i in range(len(values) - 1):
            expected = (params["a"] * values[i] + params["c"]) % params["m"]
            if expected != values[i + 1]:
                return False
                
        return True
        
    def jwt_forge_none_algorithm(self, payload: Dict[str, Any]) -> str:
        """
        JWT mit 'none' Algorithmus erstellen
        """
        header = {"alg": "none", "typ": "JWT"}
        
        header_encoded = base64.urlsafe_b64encode(
            json.dumps(header, separators=(',', ':')).encode()
        ).decode().rstrip('=')
        
        payload_encoded = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(',', ':')).encode()
        ).decode().rstrip('=')
        
        # None algorithm = empty signature
        return f"{header_encoded}.{payload_encoded}."
        
    def jwt_brute_force_secret(self, jwt_token: str, wordlist: List[str] = None) -> Optional[str]:
        """
        JWT Secret Brute Force
        """
        import jwt as pyjwt
        
        if not wordlist:
            wordlist = self.get_common_secrets()
            
        for secret in wordlist:
            try:
                decoded = pyjwt.decode(jwt_token, secret, algorithms=["HS256"])
                self.logger.info(f"JWT secret found: {secret}")
                return secret
            except pyjwt.InvalidSignatureError:
                continue
            except Exception:
                continue
                
        return None
        
    def timing_attack_simulation(self, compare_function, target: str, charset: str = None) -> str:
        """
        Timing Attack Simulation
        """
        if not charset:
            charset = string.ascii_letters + string.digits
            
        discovered = ""
        
        for position in range(20):  # Max 20 Zeichen
            timing_results = []
            
            for char in charset:
                test_string = discovered + char
                
                # Simuliere Timing-Messung
                import time
                start = time.perf_counter()
                result = compare_function(test_string, target)
                end = time.perf_counter()
                
                timing_results.append({
                    'char': char,
                    'time': end - start,
                    'result': result
                })
                
            # Sortiere nach Zeit (längste Zeit = wahrscheinlich richtig)
            timing_results.sort(key=lambda x: x['time'], reverse=True)
            
            # Wenn deutlicher Timing-Unterschied
            if timing_results[0]['time'] > timing_results[-1]['time'] * 1.1:
                discovered += timing_results[0]['char']
                self.logger.info(f"Timing attack progress: {discovered}")
            else:
                break
                
        return discovered
        
    def get_common_passwords(self) -> List[str]:
        """Häufige Passwörter für Cracking"""
        return [
            "password", "123456", "admin", "test", "guest", "user",
            "root", "toor", "pass", "secret", "login", "password123",
            "admin123", "qwerty", "abc123", "welcome", "monkey",
            "dragon", "letmein", "trustno1", "111111", "1234",
            "juice", "juiceshop", "owasp", "security", "hacker"
        ]
        
    def get_common_secrets(self) -> List[str]:
        """Häufige JWT Secrets"""
        return [
            "secret", "key", "password", "admin", "test", "jwt",
            "your-256-bit-secret", "supersecret", "mySecret",
            "juice", "juiceshop", "owasp", "", "null", "undefined",
            "default", "changeme", "secretkey", "privatekey"
        ]
        
    def _generate_bruteforce_passwords(self, length: int) -> List[str]:
        """Generiert Passwörter für Brute Force"""
        charset = string.ascii_lowercase + string.digits
        return [''.join(p) for p in itertools.product(charset, repeat=length)]
        
    def analyze_crypto_implementation(self, ciphertext: str, algorithm_hint: str = None) -> Dict[str, Any]:
        """
        Analysiert kryptographische Implementierungen auf Schwächen
        """
        analysis = {
            "weaknesses": [],
            "recommendations": [],
            "crack_attempts": []
        }
        
        # Schwache Padding-Erkennung
        if len(ciphertext) % 8 == 0:
            analysis["weaknesses"].append("Possible weak padding (8-byte blocks)")
            
        # ECB Mode Detection (bei wiederholten Blöcken)
        if self._detect_ecb_mode(ciphertext):
            analysis["weaknesses"].append("Possible ECB mode encryption")
            analysis["recommendations"].append("Use CBC or GCM mode instead")
            
        # Schwache Schlüssel-Größen
        key_size_hints = {
            16: "Possible 64-bit key (weak)",
            24: "Possible 128-bit key",
            32: "Possible 192-bit key", 
            48: "Possible 256-bit key (strong)"
        }
        
        for size, description in key_size_hints.items():
            if len(ciphertext) % size == 0:
                analysis["crack_attempts"].append(description)
                
        return analysis
        
    def _detect_ecb_mode(self, ciphertext: str) -> bool:
        """Erkennt ECB Mode anhand wiederholter Blöcke"""
        try:
            # Konvertiere zu Bytes falls Hex
            if all(c in '0123456789abcdefABCDEF' for c in ciphertext):
                data = bytes.fromhex(ciphertext)
            else:
                data = base64.b64decode(ciphertext)
                
            # Prüfe auf wiederholte 16-Byte Blöcke
            blocks = [data[i:i+16] for i in range(0, len(data), 16)]
            return len(blocks) != len(set(blocks))
        except:
            return False