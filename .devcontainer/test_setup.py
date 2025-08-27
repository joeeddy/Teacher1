#!/usr/bin/env python3
"""
Test script to verify devcontainer setup and dependency installation
"""

def test_core_dependencies():
    """Test that core Python dependencies can be imported"""
    import sys
    print(f"Python version: {sys.version}")
    
    try:
        import numpy
        print(f"✓ NumPy {numpy.__version__}")
    except ImportError as e:
        print(f"✗ NumPy: {e}")
        return False
    
    try:
        import matplotlib
        print(f"✓ Matplotlib {matplotlib.__version__}")
    except ImportError as e:
        print(f"✗ Matplotlib: {e}")
        return False
    
    try:
        import websockets
        print(f"✓ WebSockets {websockets.__version__}")
    except ImportError as e:
        print(f"✗ WebSockets: {e}")
        return False
    
    try:
        import flask
        print(f"✓ Flask {flask.__version__}")
    except ImportError as e:
        print(f"✗ Flask: {e}")
        return False
    
    return True

def test_optional_dependencies():
    """Test optional dependencies that might fail in containerized environments"""
    
    # Test audio dependencies (may fail in containers without audio)
    try:
        import pyaudio
        print(f"✓ PyAudio available")
    except ImportError as e:
        print(f"? PyAudio: {e} (Expected in containers without audio)")
    
    try:
        import pyttsx3
        print(f"✓ pyttsx3 available")
    except ImportError as e:
        print(f"? pyttsx3: {e}")
    
    try:
        import speech_recognition
        print(f"✓ SpeechRecognition available")
    except ImportError as e:
        print(f"? SpeechRecognition: {e}")
    
    # Test GUI dependencies (built-in but may be missing)
    try:
        import tkinter
        print(f"✓ Tkinter available")
    except ImportError as e:
        print(f"❌ Tkinter: {e} (BUILT-IN MODULE - install python3-tk)")
        print(f"   This is a critical built-in dependency, not an optional one")
        print(f"   Install with: sudo apt-get install python3-tk")

def test_ai_dependencies():
    """Test AI/ML dependencies"""
    try:
        import tensorflow
        print(f"✓ TensorFlow {tensorflow.__version__}")
    except ImportError as e:
        print(f"✗ TensorFlow: {e}")
        return False
    
    try:
        import spacy
        print(f"✓ spaCy {spacy.__version__}")
    except ImportError as e:
        print(f"✗ spaCy: {e}")
        return False
    
    try:
        import rasa
        print(f"✓ Rasa {rasa.__version__}")
    except ImportError as e:
        print(f"✗ Rasa: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing Teacher1 Development Environment Setup")
    print("=" * 60)
    
    core_ok = test_core_dependencies()
    print()
    
    test_optional_dependencies()
    print()
    
    ai_ok = test_ai_dependencies()
    print()
    
    if core_ok and ai_ok:
        print("✅ All critical dependencies are available!")
        print("🚀 Development environment is ready for Teacher1 project")
    else:
        print("❌ Some critical dependencies are missing")
        print("📝 Check the container setup or install missing packages")