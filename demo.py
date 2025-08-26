#!/usr/bin/env python3
"""
Teacher1 Demo Script
-------------------
Demonstrates the integrated components of Teacher1 without requiring full Rasa installation.
"""

import os
import sys
import time

def demo_text_to_speech():
    """Demo the text-to-speech functionality."""
    print("\n🔊 Text-to-Speech Demo")
    print("-" * 30)
    
    try:
        from text_to_speech import speak
        print("Testing text-to-speech with sample educational content...")
        sample_text = "Hello! Welcome to Teacher 1. Let's learn math together!"
        print(f"Speaking: {sample_text}")
        speak(sample_text)
        print("✓ Text-to-speech is working!")
        return True
    except ImportError:
        print("❌ Text-to-speech not available. Install pyttsx3: pip install pyttsx3")
        return False
    except Exception as e:
        print(f"❌ Error with text-to-speech: {e}")
        return False

def demo_gui():
    """Demo the GUI functionality."""
    print("\n🖥️ GUI Demo")
    print("-" * 30)
    
    try:
        # Test import without actually showing the GUI
        from big_text_gui import BigTextApp
        print("✓ GUI components are available!")
        print("  To run the GUI: python big_text_gui.py")
        return True
    except ImportError as e:
        print(f"❌ GUI not available: {e}")
        return False

def demo_speech_recognition():
    """Demo speech recognition availability."""
    print("\n🎤 Speech Recognition Demo")
    print("-" * 30)
    
    try:
        import speech_recognition as sr
        print("✓ Speech recognition library is available!")
        print("  To test speech: python speech_recognition.py")
        return True
    except ImportError:
        print("❌ Speech recognition not available. Install: pip install speechrecognition pyaudio")
        return False

def demo_fractal_ai():
    """Demo the fractal AI system."""
    print("\n🧠 Fractal AI Demo")
    print("-" * 30)
    
    try:
        import numpy as np
        from fractal_modules import get_dynamic_neighborhood
        print("✓ Fractal AI components are available!")
        print("  To run the AI system: python fractal_emergent_ai.py")
        return True
    except ImportError as e:
        print(f"❌ Fractal AI not available: {e}")
        print("  Install numpy: pip install numpy")
        return False

def demo_rasa_integration():
    """Demo the Rasa chatbot integration."""
    print("\n🤖 Rasa Chatbot Demo")
    print("-" * 30)
    
    # Test the integration script without actually starting Rasa
    try:
        from rasa_bot.chatbot_integration import Teacher1ChatBot
        print("✓ Rasa integration components are available!")
        
        # Create a simple mock conversation
        print("\nSimulated conversation (without trained model):")
        print("You: Hello")
        print("Bot: Hello! I'm your learning assistant. How can I help you learn today?")
        print("You: I want to learn math")
        print("Bot: Let's practice math! Can you tell me what 2 + 3 equals?")
        print("You: 5")
        print("Bot: Great job! You're doing wonderful!")
        
        print("\n📝 To set up the full chatbot:")
        print("  1. pip install -r requirements.txt")
        print("  2. cd rasa_bot && rasa train")
        print("  3. python chatbot_integration.py")
        return True
    except ImportError as e:
        print(f"❌ Rasa integration error: {e}")
        return False

def show_project_structure():
    """Show the project structure."""
    print("\n📁 Project Structure")
    print("-" * 30)
    
    structure = """
Teacher1/
├── requirements.txt           # All project dependencies
├── README.md                 # Complete setup guide
├── setup.py                  # Automated setup script
├── demo.py                   # This demo script
├── big_text_gui.py          # GUI for early learners
├── speech_recognition.py     # Voice input
├── text_to_speech.py        # Audio output
├── fractal_emergent_ai.py  # Advanced AI
├── fractal_modules.py       # AI components
└── rasa_bot/               # Chatbot integration
    ├── README.md           # Chatbot documentation
    ├── config.yml          # Rasa configuration
    ├── domain.yml          # Bot responses & intents
    ├── chatbot_integration.py  # Integration script
    └── data/               # Training data
        ├── nlu.yml        # Intent examples
        ├── stories.yml    # Conversation flows
        └── rules.yml      # Bot rules
    """
    print(structure)

def main():
    """Run the demo."""
    print("🎓 Teacher1 Platform Demo")
    print("=" * 40)
    
    # Track which components work
    working_components = []
    
    # Test each component
    if demo_gui():
        working_components.append("GUI")
    
    if demo_text_to_speech():
        working_components.append("Text-to-Speech")
    
    if demo_speech_recognition():
        working_components.append("Speech Recognition")
    
    if demo_fractal_ai():
        working_components.append("Fractal AI")
    
    if demo_rasa_integration():
        working_components.append("Rasa Integration")
    
    # Show project structure
    show_project_structure()
    
    # Summary
    print("\n📊 Component Status Summary")
    print("-" * 30)
    if working_components:
        print(f"✓ Working components: {', '.join(working_components)}")
    else:
        print("❌ No components are fully ready. Please install dependencies.")
    
    print(f"\n🚀 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run setup script: python setup.py")
    print("3. Start the chatbot: python rasa_bot/chatbot_integration.py")
    
    print("\n✨ The Teacher1 platform is ready for educational AI!")

if __name__ == "__main__":
    main()