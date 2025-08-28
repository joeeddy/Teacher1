"""
Tests for Teacher1 Web Interface
-------------------------------
Test suite for the embedded webview functionality and security features.
"""

import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from web_interface.app import Teacher1WebInterface
from web_interface.config import WebInterfaceConfig


class TestWebInterfaceConfig(unittest.TestCase):
    """Test configuration and security features"""
    
    def test_domain_validation(self):
        """Test domain whitelist validation"""
        # Test allowed domains
        allowed_urls = [
            'https://en.wikipedia.org/wiki/Science',
            'https://www.khanacademy.org/math',
            'https://simple.wikipedia.org/wiki/History'
        ]
        
        for url in allowed_urls:
            self.assertTrue(WebInterfaceConfig.is_domain_allowed(url), 
                          f"URL should be allowed: {url}")
        
        # Test disallowed domains
        disallowed_urls = [
            'https://malicious-site.com',
            'https://evil.example.com',
            'http://localhost:8080'
        ]
        
        for url in disallowed_urls:
            self.assertFalse(WebInterfaceConfig.is_domain_allowed(url), 
                           f"URL should be blocked: {url}")
    
    def test_url_sanitization(self):
        """Test URL sanitization"""
        test_cases = [
            ('http://en.wikipedia.org', 'https://en.wikipedia.org'),
            ('www.khanacademy.org', 'https://www.khanacademy.org'),
            ('https://simple.wikipedia.org/wiki/Science', 'https://simple.wikipedia.org/wiki/Science'),
        ]
        
        for input_url, expected in test_cases:
            result = WebInterfaceConfig.sanitize_url(input_url)
            self.assertEqual(result, expected, 
                           f"URL sanitization failed for {input_url}")
    
    def test_csp_header_generation(self):
        """Test Content Security Policy header generation"""
        csp = WebInterfaceConfig.get_csp_header()
        self.assertIn("default-src 'self'", csp)
        self.assertIn("frame-src", csp)
        self.assertIn("https://", csp)


class TestWebInterface(unittest.TestCase):
    """Test web interface functionality"""
    
    def setUp(self):
        """Set up test client"""
        self.web_interface = Teacher1WebInterface()
        self.app = self.web_interface.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_page(self):
        """Test that index page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Teacher1 Kindergarten Learning Assistant', response.data)
        self.assertIn(b'Educational Content', response.data)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('personalized_chatbot_available', data)
        self.assertIn('version', data)
    
    def test_chat_endpoint_basic(self):
        """Test basic chat functionality"""
        response = self.client.post('/chat',
                                  data=json.dumps({'message': 'Hello'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('message', data)
        self.assertIn('timestamp', data)
    
    def test_chat_endpoint_validation(self):
        """Test chat endpoint input validation"""
        # Test empty message
        response = self.client.post('/chat',
                                  data=json.dumps({'message': ''}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test missing message field
        response = self.client.post('/chat',
                                  data=json.dumps({}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test message too long
        long_message = 'x' * 501
        response = self.client.post('/chat',
                                  data=json.dumps({'message': long_message}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_embed_intent_detection(self):
        """Test detection of embed intents"""
        test_cases = [
            ('show me science content', 'science'),
            ('open math resources', 'math'),
            ('display history information', 'history'),
            ('show educational content about animals', 'animal'),
        ]
        
        for message, expected_topic in test_cases:
            embed_info = self.web_interface.check_for_embed_intent(message)
            self.assertIsNotNone(embed_info, f"No embed detected for: {message}")
            self.assertIn('url', embed_info)
            self.assertIn('title', embed_info)
    
    def test_fallback_responses(self):
        """Test fallback responses when chatbot is unavailable"""
        responses = [
            ('math help', 'math'),
            ('science question', 'science'),
            ('history topic', 'history'),
            ('reading help', 'reading'),
            ('hello', 'Hello'),
            ('help', 'help'),
        ]
        
        for message, expected_keyword in responses:
            response = self.web_interface.get_fallback_response(message)
            self.assertIsInstance(response, str)
            self.assertTrue(len(response) > 0)
    
    def test_security_headers(self):
        """Test security headers are applied"""
        response = self.client.get('/')
        
        # Check for security headers
        self.assertIn('Content-Security-Policy', response.headers)
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertIn('X-Frame-Options', response.headers)
        
        # Verify CSP contains expected directives
        csp = response.headers.get('Content-Security-Policy')
        self.assertIn("default-src 'self'", csp)
        self.assertIn('frame-src', csp)


class TestEmbedFunctionality(unittest.TestCase):
    """Test iframe embedding functionality"""
    
    def setUp(self):
        self.web_interface = Teacher1WebInterface()
    
    def test_science_content_mapping(self):
        """Test science content URL mapping"""
        embed_info = self.web_interface.check_for_embed_intent("show me science content")
        self.assertIsNotNone(embed_info)
        self.assertIn('wikipedia.org', embed_info['url'])
        self.assertIn('Science', embed_info['title'])
    
    def test_math_content_mapping(self):
        """Test math content URL mapping"""
        embed_info = self.web_interface.check_for_embed_intent("open math resources")
        self.assertIsNotNone(embed_info)
        self.assertIn('khanacademy.org', embed_info['url'])
        self.assertIn('Math', embed_info['title'])
    
    def test_url_safety_check(self):
        """Test URL safety validation"""
        safe_urls = [
            'https://en.wikipedia.org/wiki/Science',
            'https://www.khanacademy.org/math'
        ]
        
        unsafe_urls = [
            'https://malicious.com',
            'http://evil.example.com',
            'javascript:alert(1)'
        ]
        
        for url in safe_urls:
            self.assertTrue(self.web_interface.is_url_safe(url),
                          f"Safe URL incorrectly flagged: {url}")
        
        for url in unsafe_urls:
            self.assertFalse(self.web_interface.is_url_safe(url),
                           f"Unsafe URL incorrectly allowed: {url}")
    
    def test_direct_url_detection(self):
        """Test detection of direct URLs in messages"""
        message = "Please show https://simple.wikipedia.org/wiki/Education"
        embed_info = self.web_interface.check_for_embed_intent(message)
        self.assertIsNotNone(embed_info)
        self.assertEqual(embed_info['url'], 'https://simple.wikipedia.org/wiki/Education')


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)