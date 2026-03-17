"""
Audio Enhancement - Noise filtering and VAD (Voice Activity Detection)
Makes JARVIS work in noisy environments like cafes, offices, etc.
"""

import numpy as np
import speech_recognition as sr
from config import DEBUG_MODE

try:
    import noisereduce as nr
    HAS_NOISE_REDUCE = True
except ImportError:
    HAS_NOISE_REDUCE = False

try:
    import webrtcvad
    HAS_VAD = True
except ImportError:
    HAS_VAD = False


class AudioEnhancer:
    """Enhance audio for better speech recognition in noisy environments"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300  # Lower = more sensitive
        self.recognizer.phrase_time_limit = 10
        
        if DEBUG_MODE:
            if HAS_NOISE_REDUCE:
                print("✅ Noise reduction enabled")
            if HAS_VAD:
                print("✅ Voice Activity Detection enabled")
    
    def reduce_noise(self, audio_data):
        """
        Reduce background noise from audio
        Requires: pip install noisereduce numpy
        """
        if not HAS_NOISE_REDUCE:
            return audio_data
        
        try:
            # Convert audio to numpy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16)
            
            # Reduce noise
            reduced = nr.reduce_noise(
                y=audio_np,
                sr=16000,
                y_norm=False,
                stationary=True,
                prop_decrease=1.0
            )
            
            # Convert back to bytes
            return reduced.astype(np.int16).tobytes()
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"[WARNING] Noise reduction failed: {e}")
            return audio_data
    
    def detect_voice_activity(self, audio_data, sample_rate=16000):
        """
        Detect if audio contains speech (Voice Activity Detection)
        Returns: True if speech detected, False if silent/noise
        """
        if not HAS_VAD:
            return True
        
        try:
            vad = webrtcvad.Vad()
            vad.set_mode(2)  # 0-3, higher = more aggressive
            
            # Split audio into frames
            frame_durations = [10, 20, 30]  # milliseconds
            frame_size = int(sample_rate * frame_durations[1] / 1000) * 2
            
            frames = [audio_data[i:i+frame_size] for i in range(0, len(audio_data), frame_size)]
            
            speech_frames = 0
            for frame in frames:
                if len(frame) == frame_size:
                    is_speech = vad.is_speech(frame, sample_rate)
                    if is_speech:
                        speech_frames += 1
            
            # If >50% frames contain speech, return True
            return speech_frames > len(frames) // 2
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"[WARNING] VAD failed: {e}")
            return True
    
    def enhance_audio(self, audio_data):
        """Complete audio enhancement pipeline"""
        
        # Step 1: Reduce background noise
        audio_data = self.reduce_noise(audio_data)
        
        # Step 2: Normalize volume
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        audio_np = audio_np / np.max(np.abs(audio_np))
        audio_data = (audio_np * 32767).astype(np.int16).tobytes()
        
        return audio_data


def setup_microphone():
    """
    Optimized microphone setup for noisy environments
    """
    recognizer = sr.Recognizer()
    
    # Dynamic threshold adaptation
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 300
    
    # Longer initial silence timeout
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.3
    
    return recognizer


def install_audio_dependencies():
    """Install optional audio enhancement packages"""
    import subprocess
    import sys
    
    packages = []
    
    if not HAS_NOISE_REDUCE:
        print("[INFO] Installing noisereduce...")
        packages.append("noisereduce")
    
    if not HAS_VAD:
        print("[INFO] Installing webrtcvad...")
        packages.append("webrtcvad")
    
    if packages:
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("✅ Audio enhancement packages installed")


if __name__ == "__main__":
    # Auto-install if needed
    install_audio_dependencies()
