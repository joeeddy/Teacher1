#!/usr/bin/env python3
"""
Teacher1 Setup Script
--------------------
This script helps set up the Teacher1 project with Rasa chatbot integration.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command.split(),
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("Error: Python 3.7+ is required")
        return False
    print(f"Python version: {version.major}.{version.minor}.{version.micro} ✓")
    return True

def install_dependencies():
    """Install project dependencies."""
    print("\n📦 Installing dependencies...")
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print("Error: requirements.txt not found")
        return False
    
    result = run_command("pip install -r requirements.txt")
    return result is not None

def setup_rasa():
    """Set up and train the Rasa model."""
    print("\n🤖 Setting up Rasa chatbot...")
    
    rasa_dir = Path("rasa_bot")
    if not rasa_dir.exists():
        print("Error: rasa_bot directory not found")
        return False
    
    # Train the Rasa model
    print("Training Rasa model...")
    result = run_command("rasa train", cwd=str(rasa_dir))
    
    if result:
        print("Rasa model trained successfully! ✓")
        return True
    else:
        print("Failed to train Rasa model")
        return False

def test_components():
    """Test individual components."""
    print("\n🧪 Testing components...")
    
    # Test imports
    test_imports = [
        ("numpy", "import numpy as np; print('NumPy:', np.__version__)"),
        ("text_to_speech", "from text_to_speech import speak; print('TTS: Available')"),
        ("fractal_modules", "import fractal_modules; print('Fractal modules: Available')"),
    ]
    
    for name, test_code in test_imports:
        try:
            result = subprocess.run(
                [sys.executable, "-c", test_code],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"{name}: ✓")
                if result.stdout.strip():
                    print(f"  {result.stdout.strip()}")
            else:
                print(f"{name}: ✗")
                if result.stderr:
                    print(f"  Error: {result.stderr.strip()}")
        except Exception as e:
            print(f"{name}: ✗ (Exception: {e})")

def show_usage_examples():
    """Show usage examples."""
    print("\n📚 Usage Examples:")
    print("="*50)
    
    examples = [
        ("GUI Application", "python big_text_gui.py"),
        ("Text-to-Speech Demo", "python text_to_speech.py"),
        ("Speech Recognition Demo", "python speech_recognition.py"),
        ("Fractal AI System", "python fractal_emergent_ai.py"),
        ("Chatbot (with TTS)", "python rasa_bot/chatbot_integration.py"),
        ("Chatbot (text only)", "python rasa_bot/chatbot_integration.py --no-tts"),
        ("Rasa Shell", "cd rasa_bot && rasa shell"),
    ]
    
    for name, command in examples:
        print(f"\n{name}:")
        print(f"  {command}")

def main():
    """Main setup function."""
    print("🎓 Teacher1 Setup Script")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return 1
    
    # Setup Rasa
    if not setup_rasa():
        print("❌ Failed to setup Rasa")
        print("Note: You can manually train later with: cd rasa_bot && rasa train")
    
    # Test components
    test_components()
    
    # Show usage examples
    show_usage_examples()
    
    print("\n✅ Setup complete!")
    print("\nTo get started:")
    print("  python rasa_bot/chatbot_integration.py")
    
    return 0

if __name__ == "__main__":
    exit(main())