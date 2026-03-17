# Voice Commands Handler - Dedicated voice command processing

from voice.listen import listen_with_retry, listen_with_confirmation, voice_command_reference, get_voice_history
from voice.speak import speak
from tools.tasks import execute
import os

class VoiceCommandHandler:
    """
    Interactive voice command handler with advanced features
    """
    
    def __init__(self):
        self.running = False
        self.session_commands = []
    
    def start_voice_session(self):
        """
        Start interactive voice command session
        """
        self.running = True
        self.session_commands = []
        
        speak("Entering voice mode")
        print("\n" + "="*70)
        print("[VOICE MODE] Say your commands or type options below:")
        print("="*70)
        
        while self.running:
            self.show_voice_menu()
    
    def show_voice_menu(self):
        """
        Show voice mode menu
        """
        print("\n[VOICE OPTIONS]")
        print("1. Listen (say your command)")
        print("2. Show all commands")
        print("3. Recent commands")
        print("4. Listen with confirmation")
        print("5. Exit voice mode")
        print("-" * 70)
        print("Choose (1-5) or speak directly: ", end="")
        
        choice = input().strip().lower()
        
        if choice in ['1', 'one', 'listen', 'say command']:
            self.handle_voice_input()
        
        elif choice in ['2', 'two', 'show', 'commands', 'help']:
            self.show_command_reference()
        
        elif choice in ['3', 'three', 'history', 'recent']:
            self.show_recent_commands()
        
        elif choice in ['4', 'four', 'confirm', 'confirmation']:
            self.handle_voice_with_confirmation()
        
        elif choice in ['5', 'five', 'exit', 'quit', 'done']:
            self.exit_voice_mode()
        
        else:
            # User typed a command directly
            if choice:
                self.execute_voice_command(choice)
    
    def handle_voice_input(self):
        """
        Listen and execute voice command
        """
        print("\n[LISTENING] Say your command now...")
        speak("Listening")
        
        command = listen_with_retry(max_retries=2)
        
        if command:
            self.execute_voice_command(command)
        else:
            speak("Sorry, I didn't catch that")
            print("[ERROR] No command recognized")
    
    def handle_voice_with_confirmation(self):
        """
        Listen with user confirmation
        """
        print("\n[LISTENING] Say your command now...")
        speak("Listening")
        
        command = listen_with_confirmation()
        
        if command:
            self.execute_voice_command(command)
    
    def execute_voice_command(self, command):
        """
        Execute the voice command
        """
        print(f"\n[EXECUTING] '{command}'")
        speak(f"Executing {command}")
        
        # Process command
        response = execute(command)
        
        # Speak response
        if response:
            print(f"[RESPONSE] {response}")
            speak(response)
        
        # Add to session
        self.session_commands.append(command)
    
    def show_command_reference(self):
        """
        Display command reference
        """
        print("\n" + "="*70)
        voice_command_reference()
        print("="*70)
    
    def show_recent_commands(self):
        """
        Show recent voice commands
        """
        print("\n[RECENT COMMANDS]")
        
        # Session commands
        if self.session_commands:
            print("\n📌 This Session:")
            for i, cmd in enumerate(self.session_commands[-5:], 1):
                print(f"  {i}. {cmd}")
        
        # File history
        history = get_voice_history(limit=10)
        if history:
            print("\n📋 Command History:")
            for cmd in history[-5:]:
                print(f"  {cmd}", end="")
        else:
            print("No command history available")
    
    def exit_voice_mode(self):
        """
        Exit voice mode
        """
        self.running = False
        speak("Exiting voice mode")
        print("\n[EXIT] Goodbye!")
    
    def quick_voice_command(self):
        """
        Quick single voice command (no menu)
        """
        print("\n[QUICK VOICE] Say your command...")
        speak("Listening for command")
        
        command = listen_with_retry(max_retries=3)
        
        if command:
            print(f"[COMMAND] {command}")
            response = execute(command)
            
            if response:
                print(f"[RESPONSE] {response}")
                speak(response)
            
            return response
        else:
            speak("Sorry, I didn't understand")
            return None


def start_voice_assistant():
    """
    Start the voice assistant
    """
    handler = VoiceCommandHandler()
    handler.start_voice_session()


def quick_voice(command_type="interactive"):
    """
    Quick voice command
    
    Types:
    - "interactive": Full menu driven
    - "quick": Single command
    - "confirm": With confirmation
    """
    handler = VoiceCommandHandler()
    
    if command_type == "interactive":
        handler.start_voice_session()
    elif command_type == "quick":
        return handler.quick_voice_command()
    elif command_type == "confirm":
        handler.handle_voice_with_confirmation()


if __name__ == "__main__":
    start_voice_assistant()
