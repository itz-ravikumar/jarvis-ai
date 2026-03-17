# Speech Recognition Module - Enhanced voice to text with retry and confirmation

import speech_recognition as sr
from config import DEBUG_MODE
import os

# Voice command history
COMMAND_HISTORY_FILE = "jarvis_data/voice_commands.txt"

def listen(timeout=10, phrase_time_limit=None):
    """
    Listen to microphone and convert speech to text
    Args:
        timeout: Maximum time to wait for speech (seconds)
        phrase_time_limit: Maximum duration of phrase (seconds)
    Returns: text command from user (lowercase)
    """
    recognizer = sr.Recognizer()
    
    try:
        # Check if microphone is available
        try:
            mic = sr.Microphone()
        except (AttributeError, OSError) as e:
            if DEBUG_MODE:
                print(f"[WARNING] Microphone not detected: {e}")
            print("[TEXT MODE] Microphone not available - Using text input")
            return text_input()
        
        with mic as source:
            print("🎤 Listening...")
            
            # Adjust for ambient noise
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
            except Exception as e:
                if DEBUG_MODE:
                    print(f"⚠️  Noise adjustment warning: {e}")
            
            try:
                # Listen for audio with timeout
                audio = recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            except sr.RequestError:
                print("❌ Microphone error. Please check your microphone.")
                return ""
            except sr.WaitTimeoutError:
                print("❌ No speech detected. Using text input instead.")
                return text_input()
        
        # Try multiple recognition engines for better accuracy
        command = try_speech_recognition(recognizer, audio)
        
        if DEBUG_MODE and command:
            print(f"👤 You said: {command}")
        
        # Save to command history
        if command:
            save_voice_command(command)
        
        return command.lower() if command else ""
    
    except Exception as e:
        # Fallback to text input if microphone not available
        if DEBUG_MODE:
            print(f"⚠️  Microphone error ({type(e).__name__})")
        print("📝 Text input mode - Type your command: ", end="")
        return text_input()

def try_speech_recognition(recognizer, audio):
    """
    Try multiple speech recognition engines
    Primary: Google Speech Recognition (free, best)
    """
    
    # Primary: Google Speech Recognition
    try:
        if DEBUG_MODE:
            print("🔄 Processing speech...")
        command = recognizer.recognize_google(audio, language='en-US')
        return command
    except sr.UnknownValueError:
        print("❌ Speech not clear. Could not understand.")
        return None
    except sr.RequestError as e:
        print(f"❌ Service error: {e}")
        return None

def text_input():
    """Fallback to text input"""
    command = input().lower().strip()
    if command:
        save_voice_command(f"[TEXT] {command}")
    return command

def listen_with_retry(max_retries=3):
    """
    Listen with automatic retry on failure
    """
    for attempt in range(max_retries):
        if attempt > 0:
            print(f"\n🔄 Retry {attempt}/{max_retries - 1}")
        
        command = listen()
        
        if command:
            return command
    
    print("❌ Failed to get command after retries.")
    return ""

def listen_with_confirmation():
    """
    Listen and ask for confirmation before executing
    """
    command = listen()
    
    if command:
        print(f"\n✅ I heard: '{command}'")
        print("Execute? (yes/no/retry): ", end="")
        confirm = input().lower().strip()
        
        if confirm in ['yes', 'y']:
            return command
        elif confirm in ['retry', 'r']:
            return listen_with_confirmation()
        else:
            print("❌ Cancelled.")
            return ""
    
    return ""

def voice_command_reference():
    """
    Show available voice commands
    """
    commands = """
🎯 VOICE COMMAND REFERENCE
════════════════════════════════════════════════════════════

⏰ TIME & DATE:
  • "what time is it"
  • "what date is it"
  • "what day is today"

🔍 WEB SEARCH:
  • "search [topic]" → Google search
  • "google [query]"
  • "youtube [video]"
  • "wikipedia [topic]"

💻 APPLICATIONS:
  • "open chrome"
  • "open notepad"
  • "open calculator"
  • "open code"
  • "open chat gpt"
  • "open copilot"
  • "open stack overflow"

🤖 AI & CODING:
  • "what code" → Get Stack Overflow help
  • "explain code" → Coding assistance
  • "coding help" → Help with programming

📊 REPORTS:
  • "prepare a report on fintech AI trends"
  • "daily briefing"
  • "market trends"
  • "productivity report"
  • "wellness"
  • "career development"
  • "tech trends"

📝 TASKS:
  • "add task [task name]"
  • "list tasks"
  • "my tasks"
  • "completed tasks"
  • "task summary"

😂 FUN:
  • "tell me a joke"
  • "motivational quote"
  • "weather"

🎛️ SYSTEM:
  • "system info"
  • "volume up"
  • "volume down"
  • "lock screen"
  • "shutdown"

📌 UTILITIES:
  • "help"
  • "what can you do"
  • "today summary"

════════════════════════════════════════════════════════════
    """
    print(commands)

def save_voice_command(command):
    """
    Save voice command to history
    """
    os.makedirs("jarvis_data", exist_ok=True)
    
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(COMMAND_HISTORY_FILE, 'a') as f:
            f.write(f"[{timestamp}] {command}\n")
    except:
        pass

def get_voice_history(limit=10):
    """
    Get recent voice commands
    """
    if not os.path.exists(COMMAND_HISTORY_FILE):
        return []
    
    try:
        with open(COMMAND_HISTORY_FILE, 'r') as f:
            lines = f.readlines()
            return lines[-limit:]
    except:
        return []

def voice_mode_interactive():
    """
    Interactive voice mode with menu
    """
    while True:
        print("\n" + "="*60)
        print("🎤 VOICE MODE - Choose an option:")
        print("="*60)
        print("1. Listen for voice command")
        print("2. Show command reference")
        print("3. Show recent commands")
        print("4. Exit voice mode")
        print("="*60)
        print("Choice (1-4): ", end="")
        
        choice = input().strip()
        
        if choice == "1":
            command = listen_with_confirmation()
            if command:
                return command
        
        elif choice == "2":
            voice_command_reference()
        
        elif choice == "3":
            history = get_voice_history()
            if history:
                print("\n📋 Recent Commands:")
                for cmd in history:
                    print(f"  {cmd}", end="")
            else:
                print("No command history")
        
        elif choice == "4":
            print("👋 Exiting voice mode")
            break
        
        else:
            print("Invalid choice")
