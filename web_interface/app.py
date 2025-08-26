"""
Teacher1 Web Interface
---------------------
Flask web application that provides a web-based interface for the Teacher1 chatbot
with embedded iframe functionality for educational content.
"""

import os
import sys
import asyncio
import logging
import re
from typing import Dict, Any, Optional
from urllib.parse import urlparse

from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import configuration
from web_interface.config import WebInterfaceConfig, DEBUG, HOST, PORT

# Import chatbot
CHATBOT_AVAILABLE = False
try:
    from rasa_bot.chatbot_integration import Teacher1ChatBot
    CHATBOT_AVAILABLE = True
except ImportError:
    print("Warning: Rasa chatbot not available. Using personalized chatbot.")

# Import personalized chatbot as fallback
PERSONALIZED_CHATBOT_AVAILABLE = False
try:
    from personalized_chatbot import PersonalizedKindergartenChatbot
    PERSONALIZED_CHATBOT_AVAILABLE = True
except ImportError:
    print("Warning: Personalized chatbot not available. Web interface will run in demo mode.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Teacher1WebInterface:
    """Web interface for Teacher1 chatbot with embedded content support"""
    
    def __init__(self):
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        
        # Configure Flask
        self.app.config['SECRET_KEY'] = WebInterfaceConfig.SECRET_KEY
        self.app.config['DEBUG'] = DEBUG
        
        # Enable CORS for development
        CORS(self.app)
        
        # Initialize chatbot if available
        self.chatbot = None
        self.personalized_chatbot = None
        
        if CHATBOT_AVAILABLE:
            try:
                self.chatbot = Teacher1ChatBot()
                logger.info("Rasa chatbot initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Rasa chatbot: {e}")
                self.chatbot = None
        
        # Initialize personalized chatbot as fallback or primary
        if PERSONALIZED_CHATBOT_AVAILABLE:
            try:
                self.personalized_chatbot = PersonalizedKindergartenChatbot()
                logger.info("Personalized chatbot initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize personalized chatbot: {e}")
                self.personalized_chatbot = None
        
        # Session storage for student tracking
        self.active_sessions = {}  # session_id -> student_name
        
        # Setup routes
        self.setup_routes()
        self.setup_security_headers()
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Serve the main chat interface"""
            return render_template('index.html')
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            """Handle chat messages and return responses"""
            try:
                data = request.get_json()
                if not data or 'message' not in data:
                    return jsonify({'error': 'Invalid request format'}), 400
                
                user_message = data['message'].strip()
                if not user_message:
                    return jsonify({'error': 'Empty message'}), 400
                
                # Limit message length
                if len(user_message) > 500:
                    return jsonify({'error': 'Message too long (max 500 characters)'}), 400
                
                # Get session ID from request
                session_id = data.get('session_id', 'default')
                student_name = data.get('student_name')
                
                # Process the message
                response = self.process_message(user_message, session_id, student_name)
                return jsonify(response)
                
            except Exception as e:
                logger.error(f"Error processing chat message: {e}")
                return jsonify({'error': 'Internal server error'}), 500
        
        @self.app.route('/start_session', methods=['POST'])
        def start_session():
            """Start a new personalized learning session"""
            try:
                data = request.get_json()
                if not data or 'student_name' not in data:
                    return jsonify({'error': 'Student name required'}), 400
                
                student_name = data['student_name'].strip()
                if not student_name:
                    return jsonify({'error': 'Student name cannot be empty'}), 400
                
                session_id = data.get('session_id', 'default')
                
                if self.personalized_chatbot:
                    greeting = self.personalized_chatbot.start_session(student_name)
                    self.active_sessions[session_id] = student_name
                    
                    return jsonify({
                        'message': greeting,
                        'session_started': True,
                        'student_name': student_name,
                        'session_id': session_id
                    })
                else:
                    return jsonify({
                        'message': f"Hi {student_name}! Let's learn together!",
                        'session_started': True,
                        'student_name': student_name,
                        'session_id': session_id
                    })
                    
            except Exception as e:
                logger.error(f"Error starting session: {e}")
                return jsonify({'error': 'Failed to start session'}), 500
        
        @self.app.route('/end_session', methods=['POST'])
        def end_session():
            """End the current learning session"""
            try:
                data = request.get_json()
                session_id = data.get('session_id', 'default')
                
                if self.personalized_chatbot and session_id in self.active_sessions:
                    goodbye = self.personalized_chatbot.end_session()
                    del self.active_sessions[session_id]
                    
                    return jsonify({
                        'message': goodbye,
                        'session_ended': True
                    })
                else:
                    return jsonify({
                        'message': "Thanks for learning with me! Come back soon!",
                        'session_ended': True
                    })
                    
            except Exception as e:
                logger.error(f"Error ending session: {e}")
                return jsonify({'error': 'Failed to end session'}), 500
        
        @self.app.route('/progress/<session_id>')
        def get_progress(session_id):
            """Get student progress for the session"""
            try:
                if self.personalized_chatbot and session_id in self.active_sessions:
                    summary = self.personalized_chatbot.get_student_progress_summary()
                    return jsonify(summary)
                else:
                    return jsonify({'error': 'No active session found'}), 404
                    
            except Exception as e:
                logger.error(f"Error getting progress: {e}")
                return jsonify({'error': 'Failed to get progress'}), 500
        
        @self.app.route('/health')
        def health():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'chatbot_available': CHATBOT_AVAILABLE,
                'personalized_chatbot_available': PERSONALIZED_CHATBOT_AVAILABLE,
                'active_sessions': len(self.active_sessions),
                'version': '1.0.0'
            })
    
    def setup_security_headers(self):
        """Setup security headers for all responses"""
        
        @self.app.after_request
        def add_security_headers(response):
            # Content Security Policy
            response.headers['Content-Security-Policy'] = WebInterfaceConfig.get_csp_header()
            
            # Other security headers
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # Cache control
            if request.endpoint == 'static':
                response.headers['Cache-Control'] = 'public, max-age=31536000'
            else:
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            
            return response
    
    def process_message(self, message: str, session_id: str = 'default', student_name: str = None) -> Dict[str, Any]:
        """Process user message and return response with optional embedded content"""
        
        # Check for URL-related intents
        embed_info = self.check_for_embed_intent(message)
        
        # Use personalized chatbot if available and session is active
        if PERSONALIZED_CHATBOT_AVAILABLE and self.personalized_chatbot and session_id in self.active_sessions:
            try:
                bot_response, metadata = self.personalized_chatbot.get_response(message)
                
                response = {
                    'message': bot_response,
                    'timestamp': self.get_timestamp(),
                    'personalized': True
                }
                
                # Add metadata if available
                if metadata:
                    response.update(metadata)
                
            except Exception as e:
                logger.error(f"Personalized chatbot error: {e}")
                bot_response = self.get_fallback_response(message)
                response = {
                    'message': bot_response,
                    'timestamp': self.get_timestamp(),
                    'personalized': False
                }
        
        # Try Rasa chatbot as fallback
        elif CHATBOT_AVAILABLE and self.chatbot:
            try:
                # Use async chatbot if available
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    bot_response = loop.run_until_complete(
                        self.chatbot.get_response(message, session_id)
                    )
                finally:
                    loop.close()
                    
                response = {
                    'message': bot_response,
                    'timestamp': self.get_timestamp(),
                    'personalized': False
                }
            except Exception as e:
                logger.error(f"Chatbot error: {e}")
                bot_response = self.get_fallback_response(message)
                response = {
                    'message': bot_response,
                    'timestamp': self.get_timestamp(),
                    'personalized': False
                }
        else:
            # Fallback response
            bot_response = self.get_fallback_response(message)
            response = {
                'message': bot_response,
                'timestamp': self.get_timestamp(),
                'personalized': False
            }
        
        # Add embed information if found
        if embed_info:
            response['embed_url'] = embed_info['url']
            response['embed_title'] = embed_info['title']
        
        return response
    
    def check_for_embed_intent(self, message: str) -> Optional[Dict[str, str]]:
        """Check if message contains intent to open educational content"""
        message_lower = message.lower()
        
        # Check for direct URLs in message first (always check for URLs)
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, message)
        
        for url in urls:
            if self.is_url_safe(url):
                return {
                    'url': url,
                    'title': f'Educational Content - {urlparse(url).netloc}'
                }
        
        # Check for URL intent keywords for topic-based content
        has_url_intent = any(keyword in message_lower 
                           for keyword in WebInterfaceConfig.URL_INTENT_KEYWORDS)
        
        if not has_url_intent:
            return None
        
        # Extract educational topics and map to URLs
        educational_mappings = {
            'science': {
                'url': 'https://simple.wikipedia.org/wiki/Science',
                'title': 'Science - Simple Wikipedia'
            },
            'math': {
                'url': 'https://www.khanacademy.org/math',
                'title': 'Math - Khan Academy'
            },
            'mathematics': {
                'url': 'https://www.khanacademy.org/math',
                'title': 'Mathematics - Khan Academy'
            },
            'history': {
                'url': 'https://simple.wikipedia.org/wiki/History',
                'title': 'History - Simple Wikipedia'
            },
            'geography': {
                'url': 'https://education.nationalgeographic.org/',
                'title': 'Geography Education - National Geographic'
            },
            'animal': {
                'url': 'https://simple.wikipedia.org/wiki/Animal',
                'title': 'Animals - Simple Wikipedia'
            },
            'space': {
                'url': 'https://simple.wikipedia.org/wiki/Space',
                'title': 'Space - Simple Wikipedia'
            },
            'ocean': {
                'url': 'https://education.nationalgeographic.org/resource/ocean/',
                'title': 'Ocean Education - National Geographic'
            },
            'reading': {
                'url': 'https://www.starfall.com/',
                'title': 'Reading Games - Starfall'
            },
            'spelling': {
                'url': 'https://www.abcya.com/games/spelling',
                'title': 'Spelling Games - ABCya'
            }
        }
        
        # Look for topics in the message
        for topic, info in educational_mappings.items():
            if topic in message_lower:
                return info
        
        # Default educational content for general requests
        if any(word in message_lower for word in ['show', 'open', 'display', 'educational']):
            return {
                'url': 'https://simple.wikipedia.org/wiki/Education',
                'title': 'Education - Simple Wikipedia'
            }
        
        return None
    
    def is_url_safe(self, url: str) -> bool:
        """Check if URL is safe and allowed"""
        try:
            # Sanitize URL
            sanitized = WebInterfaceConfig.sanitize_url(url)
            if not sanitized:
                return False
            
            # Check domain whitelist
            return WebInterfaceConfig.is_domain_allowed(sanitized)
        except Exception:
            return False
    
    def get_fallback_response(self, message: str) -> str:
        """Generate fallback response when chatbot is not available"""
        message_lower = message.lower()
        
        # Educational responses
        if any(word in message_lower for word in ['math', 'mathematics', 'calculation']):
            return "I'd love to help you with math! I can show you educational math resources. Try asking me to 'show math content' or 'open math learning resources'."
        
        elif any(word in message_lower for word in ['science', 'experiment', 'physics', 'chemistry', 'biology']):
            return "Science is fascinating! I can show you educational science content. Ask me to 'display science information' or 'show science resources'."
        
        elif any(word in message_lower for word in ['history', 'historical', 'past']):
            return "History helps us understand our world! I can show you historical content. Try saying 'show history content' or 'open historical resources'."
        
        elif any(word in message_lower for word in ['read', 'reading', 'story', 'book']):
            return "Reading is fundamental! I can show you reading games and resources. Ask me to 'show reading content' or 'open reading games'."
        
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm your learning assistant. I can help you explore educational content! Try asking me to show you content about math, science, history, or reading."
        
        elif any(word in message_lower for word in ['help', 'what can you do']):
            return "I can help you learn by showing educational content! I can display websites about math, science, history, reading, and more. Just ask me to 'show content about [topic]' or 'open [topic] resources'."
        
        else:
            return "That's interesting! I can show you educational content on many topics. Try asking me to 'show educational content about science' or 'open math learning resources'."
    
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run(self, host: str = HOST, port: int = PORT, debug: bool = DEBUG):
        """Run the Flask application"""
        logger.info(f"Starting Teacher1 Web Interface on {host}:{port}")
        logger.info(f"Debug mode: {debug}")
        logger.info(f"Chatbot available: {CHATBOT_AVAILABLE}")
        
        self.app.run(host=host, port=port, debug=debug, threaded=True)

def main():
    """Main function to run the web interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Teacher1 Web Interface')
    parser.add_argument('--host', default=HOST, help='Host to bind to')
    parser.add_argument('--port', type=int, default=PORT, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', default=DEBUG, help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create and run the web interface
    web_interface = Teacher1WebInterface()
    web_interface.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()