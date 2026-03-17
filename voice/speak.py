# Text-to-Speech Module - Converts text to voice

import pyttsx3
from config import DEBUG_MODE, VOICE_SPEED, VOICE_VOLUME, ASSISTANT_NAME

# Initialize text-to-speech engine
engine = pyttsx3.init()

def setup_voice():
    """Configure voice engine properties"""
    engine.setProperty('rate', VOICE_SPEED)
    engine.setProperty('volume', VOICE_VOLUME)
    
    # Optional: Set voice (0 = male, 1 = female on most systems)
    try:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Female voice
    except:
        pass

def speak(text):
    """
    Speak out the given text using text-to-speech
    Args: text (str) - The message to speak
    """
    if DEBUG_MODE:
        print(f"🤖 {ASSISTANT_NAME}: {text}")
    
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ Speech error: {e}")

# Initialize voice on module load
setup_voice()
