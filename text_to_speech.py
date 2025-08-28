"""
Text-to-Speech for Early Learners
---------------------------------
This script reads aloud the provided text.
Requires: pyttsx3 (install with pip if needed)
"""

import pyttsx3

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)  # Set speaking speed
        engine.setProperty('volume', 1.0)  # Max volume
        
        # Try to set voice with error handling
        try:
            voices = engine.getProperty('voices')
            if voices and len(voices) > 0:
                engine.setProperty('voice', voices[0].id)  # Default voice
        except Exception as voice_error:
            print(f"Warning: Could not set voice: {voice_error}")
            print("Continuing with default system voice...")
        
        engine.say(text)
        engine.runAndWait()
        print(f"✅ Successfully spoke: {text}")
        
    except Exception as e:
        print(f"❌ Text-to-speech error: {e}")
        print(f"📝 Text was: {text}")
        print("💡 Audio output not available, but text functionality works")

if __name__ == "__main__":
    sample = "Hello! Welcome to your lesson. Let's learn and have fun together!"
    speak(sample)