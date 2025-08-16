"""
Text-to-Speech for Early Learners
---------------------------------
This script reads aloud the provided text.
Requires: pyttsx3 (install with pip if needed)
"""

import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)  # Set speaking speed
    engine.setProperty('volume', 1.0)  # Max volume
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Default voice (can be changed)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    sample = "Hello! Welcome to your lesson. Let's learn and have fun together!"
    speak(sample)