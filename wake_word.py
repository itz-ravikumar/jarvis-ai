"""
Wake Word Detection - "Hey Jarvis"
Uses Porcupine for always-on wake word detection
"""

import pvporcupine
import pyaudio
import struct
import os
from config import DEBUG_MODE


class WakeWordDetector:
    """Detects 'Hey Jarvis' wake word for always-listening mode"""
    
    def __init__(self):
        """Initialize Porcupine wake word detector"""
        self.porcupine = None
        self.pa = None
        self.stream = None
        self.is_listening = False
        
        self._initialize()
    
    def _initialize(self):
        """Initialize Porcupine and audio stream"""
        try:
            # Initialize Porcupine with 'jarvis' keyword
            self.porcupine = pvporcupine.create(
                keywords=['jarvis'],
                access_key=os.getenv("PORCUPINE_ACCESS_KEY", "")
            )
            
            # Setup audio stream
            self.pa = pyaudio.PyAudio()
            self.stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            self.is_listening = True
            if DEBUG_MODE:
                print("✅ Wake word detector initialized")
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Wake word initialization error: {e}")
            raise Exception(f"Wake word initialization failed: {e}")
    
    def listen(self):
        """Listen for wake word in background"""
        if DEBUG_MODE:
            print("🎤 Listening for 'Hey Jarvis'...")
        
        try:
            while self.is_listening:
                # Read audio frame
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm_array = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                # Process frame for wake word
                result = self.porcupine.process(pcm_array)
                
                # Wake word detected
                if result >= 0:
                    if DEBUG_MODE:
                        print("🔥 WAKE WORD DETECTED: 'Hey Jarvis'")
                    return True
        
        except KeyboardInterrupt:
            pass
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Listen error: {e}")
        
        return False
    
    def stop(self):
        """Stop listening and cleanup"""
        self.is_listening = False
        if self.stream:
            self.stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()
        
        if DEBUG_MODE:
            print("⏹️  Wake word detector stopped")


# Global detector instance
_detector = None

def initialize_wake_word():
    """Initialize global wake word detector"""
    global _detector
    if _detector is None:
        _detector = WakeWordDetector()
    return _detector


def detect_wake_word():
    """
    Listen for wake word until detected
    Returns True when 'Hey Jarvis' is detected
    """
    global _detector
    if _detector is None:
        _detector = initialize_wake_word()
    
    return _detector.listen()


def cleanup_wake_word():
    """Cleanup wake word detector"""
    global _detector
    if _detector:
        _detector.stop()
        _detector = None
