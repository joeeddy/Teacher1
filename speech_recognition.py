"""
Speech Recognition for Early Learners
-------------------------------------
This script captures speech from the microphone and prints the recognized text.
Requires: speechrecognition, pyaudio (install with pip if needed)
"""

import speech_recognition as sr

def listen_and_print():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("Say something!")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError:
        print("Sorry, there was a problem connecting to the recognition service.")

if __name__ == "__main__":
    listen_and_print()