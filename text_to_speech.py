"""
Text-to-Speech for Early Learners
---------------------------------
This script reads aloud the provided text.
Requires: pyttsx3 (install with pip if needed)
"""

import pyttsx3
import logging

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)  # Set speaking speed
        engine.setProperty('volume', 1.0)  # Max volume
        
        # Try to set a voice, but handle gracefully if no voices available
        try:
            voices = engine.getProperty('voices')
            if voices and len(voices) > 0:
                # Use the first available voice
                engine.setProperty('voice', voices[0].id)
            else:
                print("No voices found, using default TTS settings")
        except Exception as voice_error:
            print(f"Voice setting failed (continuing with default): {voice_error}")
        
        engine.say(text)
        engine.runAndWait()
        return True
        
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        print(f"Fallback - displaying text: {text}")
        return False

if __name__ == "__main__":
    sample = "Hello! Welcome to your lesson. Let's learn and have fun together!"
    success = speak(sample)
    if success:
        print("✓ Text-to-speech working properly!")
    else:
        print("⚠️ Text-to-speech had issues but provided fallback")