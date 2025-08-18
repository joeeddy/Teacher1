"""
Web Interface Configuration
--------------------------
Configuration settings for the Teacher1 web interface including
security settings and allowed domains for the embedded iframe.
"""

import os
from typing import List, Dict, Any

class WebInterfaceConfig:
    """Configuration class for the web interface"""
    
    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'teacher1-development-key-change-in-production')
    
    # Allowed domains for iframe embedding (whitelist approach for security)
    ALLOWED_DOMAINS = [
        'en.wikipedia.org',
        'simple.wikipedia.org',
        'www.khanacademy.org',
        'education.nationalgeographic.org',
        'www.mathplayground.com',
        'www.ixl.com',
        'www.abcya.com',
        'www.funbrain.com',
        'pbskids.org',
        'www.starfall.com',
        'www.education.com',
        'www.coolmath4kids.com',
        'www.multiplication.com',
        'www.mathgames.com',
        'www.teachingchannel.org',
        'www.commoncore.org'
    ]
    
    # Educational intent keywords that might trigger URL opening
    URL_INTENT_KEYWORDS = [
        'show me', 'show', 'open', 'visit', 'go to', 'display', 'load',
        'educational content', 'learning resource', 'website',
        'information about', 'learn more', 'explore'
    ]
    
    # Default iframe settings
    IFRAME_CONFIG = {
        'width': '100%',
        'height': '600px',
        'sandbox': 'allow-scripts allow-same-origin allow-forms',
        'loading': 'lazy',
        'referrerpolicy': 'strict-origin-when-cross-origin'
    }
    
    # Content Security Policy
    CSP_POLICY = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'frame-src': f"https://{' https://'.join(ALLOWED_DOMAINS)}",
        'connect-src': "'self' ws: wss:"
    }
    
    @classmethod
    def is_domain_allowed(cls, url: str) -> bool:
        """Check if a domain is in the allowed list"""
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # Remove www. prefix for comparison
            domain_clean = domain.replace('www.', '') if domain.startswith('www.') else domain
            
            for allowed in cls.ALLOWED_DOMAINS:
                allowed_clean = allowed.replace('www.', '') if allowed.startswith('www.') else allowed
                if domain == allowed or domain_clean == allowed_clean:
                    return True
            return False
        except Exception:
            return False
    
    @classmethod
    def sanitize_url(cls, url: str) -> str:
        """Sanitize and validate URL"""
        from urllib.parse import urlparse, urlunparse
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed = urlparse(url)
            # Only allow https for security
            if parsed.scheme != 'https':
                parsed = parsed._replace(scheme='https')
            
            return urlunparse(parsed)
        except Exception:
            return ""
    
    @classmethod
    def get_csp_header(cls) -> str:
        """Get Content Security Policy header string"""
        return '; '.join([f"{key} {value}" for key, value in cls.CSP_POLICY.items()])

# Development settings
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
HOST = os.environ.get('HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', 5000))