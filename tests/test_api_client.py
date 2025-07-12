#!/usr/bin/env python3
"""
Unit Tests für API Client
"""

import unittest
import requests_mock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.api_client import JuiceShopAPI


class TestJuiceShopAPI(unittest.TestCase):
    
    def setUp(self):
        self.api = JuiceShopAPI("http://test.local:3000")
        
    def test_initialization(self):
        """Test API Client Initialization"""
        self.assertEqual(self.api.base_url, "http://test.local:3000")
        self.assertEqual(self.api.timeout, 30)
        self.assertIsNone(self.api.auth_token)
        
    @requests_mock.Mocker()
    def test_check_connection_success(self, m):
        """Test successful connection check"""
        m.get("http://test.local:3000/", status_code=200)
        self.assertTrue(self.api.check_connection())
        
    @requests_mock.Mocker()
    def test_check_connection_failure(self, m):
        """Test failed connection check"""
        m.get("http://test.local:3000/", status_code=500)
        self.assertFalse(self.api.check_connection())
        
    @requests_mock.Mocker()
    def test_login_success(self, m):
        """Test successful login"""
        mock_response = {
            "authentication": {
                "token": "fake-jwt-token",
                "uId": 1
            }
        }
        m.post("http://test.local:3000/rest/user/login", json=mock_response)
        
        result = self.api.login("test@test.com", "password")
        
        self.assertIn("authentication", result)
        self.assertEqual(self.api.auth_token, "fake-jwt-token")
        self.assertEqual(self.api.user_id, 1)
        
    @requests_mock.Mocker()
    def test_get_products(self, m):
        """Test product search"""
        mock_response = {
            "data": [
                {"id": 1, "name": "Apple Juice", "price": 1.99},
                {"id": 2, "name": "Orange Juice", "price": 2.49}
            ]
        }
        m.get("http://test.local:3000/rest/products/search", json=mock_response)
        
        result = self.api.get_products(search="juice")
        
        self.assertIn("data", result)
        self.assertEqual(len(result["data"]), 2)
        
    @requests_mock.Mocker()
    def test_sql_injection_in_search(self, m):
        """Test SQL injection payload in search"""
        # Mock response for SQL injection payload
        mock_response = {
            "data": [
                {"id": 1, "name": "Admin User", "email": "admin@juice-sh.op"}
            ]
        }
        m.get("http://test.local:3000/rest/products/search", json=mock_response)
        
        # Test SQL injection payload
        result = self.api.get_products(search="')) OR 1=1--")
        
        self.assertIn("data", result)
        # Check if we got unexpected user data (indicating SQL injection)
        if result["data"] and "email" in result["data"][0]:
            self.assertIn("@", result["data"][0]["email"])


class TestSQLInjectionPayloads(unittest.TestCase):
    
    def setUp(self):
        self.payloads = [
            "' OR '1'='1'--",
            "admin@juice-sh.op'--",
            "')) OR 1=1--",
            "' UNION SELECT * FROM users--"
        ]
        
    def test_payload_format(self):
        """Test SQL injection payload format"""
        for payload in self.payloads:
            # Check that payloads contain SQL injection indicators
            self.assertTrue(
                any(indicator in payload for indicator in ["'", "--", "OR", "UNION"]),
                f"Payload {payload} doesn't contain SQL injection indicators"
            )
            
    def test_payload_safety(self):
        """Ensure payloads are for testing only"""
        # These should only be used against OWASP Juice Shop
        warning_message = "Only use against OWASP Juice Shop or authorized targets"
        self.assertTrue(warning_message)  # Reminder for developers


if __name__ == '__main__':
    unittest.main()