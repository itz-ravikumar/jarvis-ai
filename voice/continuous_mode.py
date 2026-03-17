"""
Continuous Listening Mode - Siri-style hands-free interaction
Listen for wake word → execute commands → keep listening until told to stop
"""

from voice.listen import listen_with_retry
from voice.speak import speak
from tools.tasks import execute
from brain.agent import think
from brain.memory import save_memory
from config import DEBUG_MODE, ASSISTANT_NAME
import time


def continuous_wake_word_mode():
    """
    Continuous listening mode - like Siri on iPhone
    
    Flow:
    1. Listen for "Hey Jarvis"
    2. Say "Yes?" when detected
    3. Listen for commands in loop
    4. Execute each command
    5. Keep listening until user says "stop listening"
    """
    
    from wake_word import initialize_wake_word, detect_wake_word
    
    print("\n" + "="*60)
    print(f"[{ASSISTANT_NAME}] Continuous Listening Mode Active")
    print("="*60)
    speak(f"{ASSISTANT_NAME} is listening. Say Hey {ASSISTANT_NAME} when ready.")
    print("[INFO] Waiting for wake word... (Say 'Hey Jarvis')")
    print("[INFO] Press Ctrl+C to exit")
    print("="*60 + "\n")
    
    try:
        while True:
            # >>> STEP 1: Listen for wake word
            if detect_wake_word():
                speak("Yes?")
                print(f"\n🔥 [{ASSISTANT_NAME}] Listening for commands...\n")
                
                command_count = 0
                
                # >>> STEP 2: Command execution loop
                while True:
                    command_count += 1
                    
                    # Listen for command
                    print(f"[COMMAND #{command_count}] Listening...")
                    command = listen_with_retry(max_retries=1)
                    
                    if not command:
                        # Silence detected
                        break
                    
                    print(f"[COMMAND #{command_count}] '{command}'")
                    
                    # >>> Check for stop command
                    if any(word in command.lower() for word in ["stop listening", "stop", "exit", "goodbye", "sleep"]):
                        speak("Going back to sleep")
                        print(f"[{ASSISTANT_NAME}] Returning to wake word mode\n")
                        break
                    
                    # >>> Execute command with thinking
                    try:
                        # Let AI reason about the command
                        reasoning = think(command)
                        if DEBUG_MODE and reasoning:
                            print(f"[AI REASONING] {reasoning}\n")
                        
                        # Execute
                        response = execute(command)
                        
                        if response:
                            print(f"[RESPONSE] {response}\n")
                            speak(response)
                            
                            # Save to memory
                            save_memory(command, response)
                        else:
                            speak("Command not recognized")
                    
                    except Exception as e:
                        if DEBUG_MODE:
                            print(f"[ERROR] {e}")
                        speak("There was an error")
                    
                    time.sleep(0.5)  # Brief pause between commands
    
    except KeyboardInterrupt:
        print("\n[INFO] Continuous mode interrupted by user")
        speak("Shutting down")


def smart_hybrid_mode():
    """
    Hybrid execution mode - uses smart agent for complex tasks
    
    Logic:
    - Simple commands: fast execution
    - Complex tasks: AI agent planning
    """
    
    from voice.listen import listen_with_retry
    from brain.smart_agent import execute_smart_task
    
    print("\n" + "="*60)
    print(f"[{ASSISTANT_NAME}] Smart Hybrid Mode")
    print("="*60)
    speak("Entering smart hybrid mode. I can handle complex tasks now.")
    print("[INFO] Try: 'prepare a report', 'automate workflow', etc")
    print("="*60 + "\n")
    
    while True:
        print("[INPUT] Listening...")
        command = listen_with_retry(max_retries=2)
        
        if not command:
            continue
        
        if any(word in command.lower() for word in ["stop", "exit", "goodbye"]):
            speak("Goodbye")
            break
        
        # >>> Intelligent routing
        if any(keyword in command.lower() for keyword in ["create", "build", "analyze", "prepare", "automate", "generate", "report"]):
            # Complex task → use smart agent
            print(f"[SMART AGENT] Processing: {command}")
            speak("Processing your request with AI planning...")
            response = execute_smart_task(command)
        else:
            # Simple command → fast execution
            print(f"[FAST EXECUTION] Processing: {command}")
            response = execute(command)
        
        if response:
            print(f"[RESULT] {response}\n")
            speak(response)


def short_response_style():
    """
    Convert long responses to Siri-style short responses
    
    Before: "Opening Google Chrome browser application now"
    After: "Opening Chrome"
    """
    
    response_shortcuts = {
        # Apps
        "opening google chrome": "opening chrome",
        "opening chrome browser": "opening chrome",
        "launching google chrome": "opening chrome",
        "opening firefox": "opening firefox",
        "opening notepad": "opening notepad",
        "opening visual studio code": "opening vs code",
        
        # Search
        "searching google for": "searching for",
        "searching wikipedia for": "searching",
        "searching youtube for": "searching",
        
        # Time
        "the current time is": "it's",
        "the current date is": "today is",
        
        # Volume
        "volume increased": "volume up",
        "volume decreased": "volume down",
        "system volume": "volume changed",
    }
    
    return response_shortcuts


def apply_siri_style(response):
    """Apply Siri-style formatting to response"""
    
    if not response:
        return response
    
    shortcuts = short_response_style()
    
    # Apply shortcuts
    for long_form, short_form in shortcuts.items():
        if long_form in response.lower():
            response = response.lower().replace(long_form, short_form)
            break
    
    # Truncate to first sentence for brevity
    response = response.split(".")[0]
    
    # Remove redundant words
    response = response.replace("now", "").replace("please", "").strip()
    
    return response


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "continuous":
            continuous_wake_word_mode()
        elif mode == "hybrid":
            smart_hybrid_mode()
    else:
        continuous_wake_word_mode()
