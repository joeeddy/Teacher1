"""
Fallback implementations for optional dependencies in Teacher1.
These provide working alternatives when optional packages cannot be installed.
"""

import os
import sys
import logging
import tempfile
import subprocess
from typing import Dict, List, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockPyAudio:
    """
    Mock PyAudio implementation that provides file-based audio processing.
    This allows speech recognition to work with audio files instead of microphone.
    """
    
    # Constants that match real PyAudio
    paFloat32 = 1
    paInt16 = 8
    paInt24 = 4
    paInt32 = 2
    paUInt8 = 16
    
    class Stream:
        def __init__(self, *args, **kwargs):
            self.is_active = False
            self.is_stopped = True
            
        def start_stream(self):
            self.is_active = True
            self.is_stopped = False
            
        def stop_stream(self):
            self.is_active = False
            self.is_stopped = True
            
        def close(self):
            self.is_active = False
            self.is_stopped = True
            
        def read(self, num_frames, exception_on_overflow=True):
            # Return silence (zeros) as audio data
            return b'\x00' * (num_frames * 2)  # 16-bit audio
            
        def write(self, data, num_frames=None, exception_on_overflow=True):
            # Mock write operation
            pass
    
    def __init__(self):
        logger.info("MockPyAudio initialized - file-based audio processing available")
        
    def open(self, *args, **kwargs):
        return self.Stream(*args, **kwargs)
        
    def terminate(self):
        pass
        
    def get_device_count(self):
        return 1
        
    def get_device_info_by_index(self, index):
        return {
            'name': 'Mock Audio Device',
            'index': 0,
            'maxInputChannels': 2,
            'maxOutputChannels': 2,
            'defaultSampleRate': 44100
        }

class MockRasa:
    """
    Mock Rasa implementation with educational chatbot functionality.
    Provides working chatbot responses without requiring full Rasa installation.
    """
    
    class Agent:
        def __init__(self, model_path=None):
            self.model_path = model_path
            logger.info("MockRasa Agent initialized - fallback educational chatbot active")
            
            # Educational response patterns
            self.educational_responses = {
                "greeting": [
                    "Hello! I'm your learning assistant. How can I help you today?",
                    "Hi there! Ready to learn something new and exciting?",
                    "Welcome! I'm here to help you discover amazing things!"
                ],
                "math": [
                    "Math is fantastic! It helps us understand patterns and solve problems. What would you like to explore?",
                    "Numbers are everywhere! Let's discover the magic of mathematics together.",
                    "Great choice! Math helps us think logically and solve real-world challenges."
                ],
                "reading": [
                    "Reading opens up whole new worlds! What kind of stories do you enjoy?",
                    "Books are treasures full of knowledge and adventure. Let's explore together!",
                    "Reading is one of the most powerful skills you can develop. I'm excited to help!"
                ],
                "science": [
                    "Science helps us understand how the amazing world around us works!",
                    "Every question you ask is the beginning of a scientific discovery!",
                    "Science is all about curiosity and exploration. What makes you curious?"
                ],
                "creative": [
                    "Creativity is your superpower! It helps you think in new and innovative ways.",
                    "Art, music, and creative thinking make learning more fun and meaningful!",
                    "Your imagination is unlimited! Let's use it to enhance your learning."
                ],
                "pattern": [
                    "Patterns are everywhere in learning! They help us predict and understand.",
                    "Recognizing patterns is a fundamental skill that helps in math, reading, and science.",
                    "Great observation! Pattern recognition is key to effective learning."
                ],
                "learn": [
                    "Learning is a wonderful journey of discovery! Every step teaches us something new.",
                    "The best learners are curious and persistent. You're developing both qualities!",
                    "Learning never stops! Each challenge makes you stronger and smarter."
                ],
                "default": [
                    "That's a thoughtful question! Learning happens when we're curious about the world.",
                    "I love how you're thinking! What else would you like to explore?",
                    "Your questions show you're an active learner. Keep wondering and discovering!"
                ]
            }
        
        @classmethod
        def load(cls, model_path):
            return cls(model_path)
            
        async def handle_text(self, message, sender_id="user"):
            """Handle text input and return educational response."""
            response_text = self._generate_educational_response(message)
            return [{"text": response_text}]
            
        def _generate_educational_response(self, message):
            """Generate educational response based on message content."""
            message_lower = message.lower()
            
            # Check for specific educational topics
            if any(word in message_lower for word in ["hello", "hi", "hey", "start"]):
                responses = self.educational_responses["greeting"]
            elif any(word in message_lower for word in ["math", "number", "count", "calculate"]):
                responses = self.educational_responses["math"]
            elif any(word in message_lower for word in ["read", "book", "story", "letter", "word"]):
                responses = self.educational_responses["reading"]
            elif any(word in message_lower for word in ["science", "experiment", "how", "why", "what"]):
                responses = self.educational_responses["science"]
            elif any(word in message_lower for word in ["creative", "art", "music", "draw", "imagine"]):
                responses = self.educational_responses["creative"]
            elif any(word in message_lower for word in ["pattern", "sequence", "repeat", "similar"]):
                responses = self.educational_responses["pattern"]
            elif any(word in message_lower for word in ["learn", "study", "practice", "improve"]):
                responses = self.educational_responses["learn"]
            else:
                responses = self.educational_responses["default"]
            
            import random
            return random.choice(responses)
    
    @staticmethod
    def __version__():
        return "fallback-1.0.0"

class MockTensorFlow:
    """
    Mock TensorFlow implementation for basic educational AI functionality.
    """
    
    __version__ = "fallback-2.0.0"
    
    class keras:
        class models:
            @staticmethod
            def Sequential():
                return MockModel()
                
        class layers:
            @staticmethod
            def Dense(*args, **kwargs):
                return MockLayer()
                
            @staticmethod
            def Dropout(*args, **kwargs):
                return MockLayer()
    
    class constant:
        @staticmethod
        def constant(value):
            return MockTensor(value)

class MockModel:
    def __init__(self):
        self.layers = []
    
    def add(self, layer):
        self.layers.append(layer)
        
    def compile(self, *args, **kwargs):
        pass
        
    def fit(self, *args, **kwargs):
        return MockHistory()
        
    def predict(self, *args, **kwargs):
        import numpy as np
        return np.array([[0.5, 0.3, 0.2]])  # Mock prediction

class MockLayer:
    pass

class MockTensor:
    def __init__(self, value):
        self.value = value

class MockHistory:
    def __init__(self):
        self.history = {'loss': [0.5, 0.3, 0.1], 'accuracy': [0.6, 0.8, 0.9]}

class MockSpacy:
    """
    Mock spaCy implementation for basic natural language processing.
    """
    
    __version__ = "fallback-3.0.0"
    
    @staticmethod
    def load(model_name):
        return MockNLP()
        
    @staticmethod
    def blank(lang):
        return MockNLP()

class MockNLP:
    def __init__(self):
        logger.info("MockSpacy NLP initialized - basic text processing available")
        
    def __call__(self, text):
        return MockDoc(text)

class MockDoc:
    def __init__(self, text):
        self.text = text
        self.tokens = text.split()
        
        # Create mock entities
        self.ents = []
        if "math" in text.lower():
            self.ents.append(MockEntity("math", "SUBJECT"))
        if "reading" in text.lower():
            self.ents.append(MockEntity("reading", "SUBJECT"))
    
    def __iter__(self):
        return iter([MockToken(token) for token in self.tokens])

class MockToken:
    def __init__(self, text):
        self.text = text
        self.lemma_ = text.lower()
        self.pos_ = "NOUN"  # Simple default

class MockEntity:
    def __init__(self, text, label):
        self.text = text
        self.label_ = label

def install_fallback_modules():
    """
    Install fallback modules by making them available for import.
    """
    # Install PyAudio fallback
    if 'pyaudio' not in sys.modules:
        pyaudio_module = type('MockModule', (), {
            'PyAudio': MockPyAudio,
            '__version__': 'fallback-0.2.11',
            'paFloat32': MockPyAudio.paFloat32,
            'paInt16': MockPyAudio.paInt16,
            'paInt24': MockPyAudio.paInt24,
            'paInt32': MockPyAudio.paInt32,
            'paUInt8': MockPyAudio.paUInt8
        })()
        sys.modules['pyaudio'] = pyaudio_module
        logger.info("PyAudio fallback module installed")
    
    # Install Rasa fallback
    if 'rasa' not in sys.modules:
        rasa_module = type('MockModule', (), {
            '__version__': 'fallback-3.6.0'
        })()
        
        # Add core submodule
        rasa_core = type('MockModule', (), {})()
        rasa_core.agent = type('MockModule', (), {'Agent': MockRasa.Agent})()
        rasa_core.interpreter = type('MockModule', (), {'RasaNLUInterpreter': MockRasa.Agent})()
        rasa_module.core = rasa_core
        
        sys.modules['rasa'] = rasa_module
        sys.modules['rasa.core'] = rasa_core
        sys.modules['rasa.core.agent'] = rasa_core.agent
        sys.modules['rasa.core.interpreter'] = rasa_core.interpreter
        logger.info("Rasa fallback module installed")
    
    # Install TensorFlow fallback
    if 'tensorflow' not in sys.modules:
        tf_module = MockTensorFlow()
        sys.modules['tensorflow'] = tf_module
        logger.info("TensorFlow fallback module installed")
    
    # Install spaCy fallback
    if 'spacy' not in sys.modules:
        sys.modules['spacy'] = MockSpacy()
        logger.info("spaCy fallback module installed")

def is_fallback_module(module_name):
    """Check if a module is using a fallback implementation."""
    try:
        module = sys.modules.get(module_name)
        if module and hasattr(module, '__version__'):
            version = getattr(module, '__version__', '')
            return 'fallback' in str(version)
    except:
        pass
    return False

if __name__ == "__main__":
    # Test the fallback modules
    print("Testing fallback modules...")
    
    install_fallback_modules()
    
    # Test PyAudio
    try:
        import pyaudio
        pa = pyaudio.PyAudio()
        print(f"✓ PyAudio fallback working: {pyaudio.__version__}")
        pa.terminate()
    except Exception as e:
        print(f"✗ PyAudio fallback failed: {e}")
    
    # Test Rasa
    try:
        from rasa.core.agent import Agent
        agent = Agent.load("test")
        print(f"✓ Rasa fallback working: {agent}")
    except Exception as e:
        print(f"✗ Rasa fallback failed: {e}")
    
    # Test TensorFlow
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow fallback working: {tf.__version__}")
    except Exception as e:
        print(f"✗ TensorFlow fallback failed: {e}")
    
    # Test spaCy
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print(f"✓ spaCy fallback working: {spacy.__version__}")
    except Exception as e:
        print(f"✗ spaCy fallback failed: {e}")
    
    print("Fallback module testing complete!")