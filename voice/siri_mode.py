# Siri-like Voice Mode - Always Listening Voice Assistant

import threading
import time
from voice.listen import listen_with_retry, get_voice_history, save_voice_command
from voice.speak import speak
from tools.tasks import execute
from config import DEBUG_MODE

class SiriMode:
    """
    Siri-like voice assistant with always-listening mode
    - Continuous listening
    - Wake word detection ("Hey Jarvis")
    - Real-time visual feedback
    - Voice responses
    """
    
    def __init__(self):
        self.running = False
        self.listening = False
        self.processing = False
        self.last_command = None
        self.command_count = 0
    
    def display_header(self):
        """Display Siri-like header"""
        print("\n" + "="*70)
        print("[SIRI MODE] Always-listening voice assistant")
        print("="*70)
        print("Activation: Say 'Hey Jarvis' or just speak")
        print("Exit: Say 'stop', 'exit', 'bye', 'goodbye'")
        print("-"*70)
        print()
    
    def show_status(self, status="listening", message=""):
        """Show real-time status like Siri"""
        if status == "listening":
            print("\r[@] Listening... (Speak now)", end="", flush=True)
        elif status == "processing":
            print("\r[*] Processing...", end="", flush=True)
        elif status == "speaking":
            print("\r[>] Speaking...", end="", flush=True)
        elif status == "done":
            print(f"\r[OK] {message}                    ")
    
    def start_siri_mode(self):
        """Main Siri mode loop"""
        self.running = True
        self.command_count = 0
        
        speak("Siri mode activated. Say Hey Jarvis to start.")
        self.display_header()
        
        try:
            while self.running:
                self.listening = True
                self.show_status("listening")
                
                # Listen for command with auto-retry
                command = listen_with_retry(max_retries=2)
                
                if not command:
                    print("\r[!] Command not detected                ", flush=True)
                    continue
                
                print(f"\r[you] {command}                    ")
                self.command_count += 1
                
                # Check for exit commands
                if any(x in command.lower() for x in ["stop", "exit", "bye", "goodbye", "quit"]):
                    speak("Goodbye!")
                    print("\n[EXIT] Siri mode deactivated\n")
                    break
                
                # Process command
                self.listening = False
                self.processing = True
                self.show_status("processing")
                
                try:
                    response = execute(command)
                    
                    if response:
                        self.processing = False
                        self.show_status("speaking")
                        print(f"\r[jarvis] {response}                    ")
                        speak(response)
                        self.show_status("done", response[:50])
                        
                        # Log command
                        save_voice_command(command)
                        
                        # Pause before next listen
                        time.sleep(1)
                    else:
                        print("\r[!] No response                        ")
                
                except Exception as e:
                    print(f"\r[ERROR] {str(e)[:60]}                    ")
                    speak(f"Error: {str(e)}")
        
        except KeyboardInterrupt:
            print("\n\n[INTERRUPT] Siri mode stopped")
            speak("Mode stopped")
        
        finally:
            self.running = False
            print(f"\n[STATS] Commands processed: {self.command_count}")
    
    def show_quick_commands(self):
        """Show quick command reference"""
        commands = [
            ("Voice Commands", [
                "'what time is it'",
                "'tell me a joke'",
                "'search [topic]'",
                "'open chrome'",
                "'weather'",
                "'prepare report'"
            ]),
            ("Control", [
                "'volume up'",
                "'volume down'",
                "'lock screen'",
            ]),
            ("Reports", [
                "'daily briefing'",
                "'market trends'",
                "'productivity report'"
            ]),
            ("Tasks", [
                "'add task [name]'",
                "'list tasks'",
                "'task summary'"
            ]),
        ]
        
        print("\n" + "="*70)
        print("[QUICK COMMANDS]")
        print("="*70)
        
        for category, cmds in commands:
            print(f"\n{category}")
            for cmd in cmds:
                print(f"   -> {cmd}")
        
        print("\n" + "="*70 + "\n")


def start_siri_mode():
    """Start Siri-like voice assistant"""
    siri = SiriMode()
    siri.start_siri_mode()


def siri_mode_with_feedback():
    """Siri mode with enhanced visual feedback"""
    from config import ASSISTANT_NAME
    
    print("\n" + "#"*70)
    print(f"#  {ASSISTANT_NAME} SIRI MODE - Voice Assistant")
    print("#"*70)
    print("\n[READY] Listening for voice commands...")
    print("[TIPS]  Say 'Hey Jarvis' to activate")
    print("[EXIT]  Say 'stop' or 'goodbye' to exit")
    print("-"*70 + "\n")
    
    siri = SiriMode()
    siri.show_quick_commands()
    siri.start_siri_mode()


# ============================================================
# MINIMAL SIRI MODE - Super Simple
# ============================================================

def minimal_siri_mode():
    """Minimal Siri mode - just listen and respond"""
    print("\n[Siri Mode] Say your command (type 'stop' to exit)\n")
    
    while True:
        print("[You] ", end="", flush=True)
        command = input().strip().lower()
        
        if command in ['stop', 'exit', 'bye', 'quit']:
            print("[Jarvis] Goodbye!")
            break
        
        if not command:
            continue
        
        print("[Processing...]", end="", flush=True)
        response = execute(command)
        print("\r" + " "*50 + "\r")
        
        if response:
            print(f"[Jarvis] {response}\n")
