#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS - Voice-Controlled AI Assistant (FULL PRODUCTION VERSION)
Advanced AI assistant with: wake word detection, smart agent, memory system, background service
"""

import sys
import os

# Fix Unicode encoding on Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core imports
from voice.listen import listen
from voice.speak import speak
from tools.tasks import execute
from brain.agent import think, intent_detection
from config import DEBUG_MODE, ASSISTANT_NAME
from voice.conversation import start_conversation_mode

# NEW: Advanced features
from brain.memory import recall_memory, save_memory, get_user_preferences
from brain.smart_agent import execute_smart_task
from wake_word import detect_wake_word, cleanup_wake_word
import threading

def display_welcome():
    """Display welcome message"""
    print("\n" + "="*60)
    print(f"[AI] Welcome to {ASSISTANT_NAME} AI Assistant - PRODUCTION")
    print("="*60)
    print("[MAIN MENU]")
    print("   1. Text commands (type commands)")
    print("   2. Voice mode (interactive menu)")
    print("   3. Quick voice (single command)")
    print("   4. Conversation mode (back & forth talking) ⭐")
    print("   5. Siri mode (always-listening)")
    print("   6. Wake word mode (say 'Hey Jarvis') 🔥")
    print("   7. Smart agent mode (multi-step tasks)")
    print("   8. Show all commands")
    print("   9. Settings")
    print("   10. Exit")
    print("="*60)
    print("\n[NEW FEATURES]")
    print("   ✅ Wake word detection - 'Hey Jarvis'")
    print("   ✅ Memory system - Learns your preferences")
    print("   ✅ Smart agent - Multi-step task automation")
    print("   ✅ Background service - Always running")
    print("="*60)
    print("\n[EXAMPLE COMMANDS]")
    print("   - 'search [query]' - Search Google")
    print("   - 'open chrome' - Launch Chrome browser")
    print("   - 'prepare fintech report' - Generate report")
    print("   - 'Remember that I like dark mode' - Save preference")
    print("="*60 + "\n")
    print("   - 'open chrome' - Launch Chrome browser")
    print("   - 'tell me a joke' - Get a joke")
    print("   - 'what time is it' - Current time")
    print("   - 'prepare fintech report' - Generate report")
    print("="*60 + "\n")

def jarvis_loop():
    """Main Jarvis event loop with menu"""
    speak(f"{ASSISTANT_NAME} is online")
    
    try:
        while True:
            print("\n[INPUT] Choose mode (1-10) or type command: ", end="")
            user_input = input().strip().lower()
            
            if not user_input:
                continue
            
            # Handle menu options
            if user_input in ['1', 'text', 'text mode', 'text commands']:
                print("[MODE] Text command mode")
                speak("Entering text command mode")
                exit_main = text_mode_loop()
                if exit_main:
                    break
            
            elif user_input in ['2', 'voice', 'voice mode']:
                print("[MODE] Voice mode")
                speak("Entering voice mode")
                from voice.voice_commands import start_voice_assistant
                try:
                    start_voice_assistant()
                except Exception as e:
                    print(f"[ERROR] Voice mode error: {e}")
            
            elif user_input in ['3', 'quick', 'quick voice']:
                print("[MODE] Quick voice command")
                speak("Listening for your command")
                from voice.listen import listen_with_retry
                command = listen_with_retry(max_retries=2)
                if command:
                    response = execute(command)
                    if response:
                        speak(response)
            
            elif user_input in ['4', 'conversation', 'talk', 'chat', 'convo']:
                print("[MODE] Conversation mode - Two-way voice dialogue")
                speak("Entering conversation mode")
                try:
                    start_conversation_mode()
                except Exception as e:
                    print(f"[ERROR] Conversation mode error: {e}")
                    speak("Error in conversation mode. Please try again.")
            
            elif user_input in ['5', 'siri', 'siri mode', 'always listen']:
                print("[MODE] Siri mode (always-listening)")
                speak("Entering Siri mode")
                from voice.siri_mode import start_siri_mode
                try:
                    start_siri_mode()
                except Exception as e:
                    print(f"[ERROR] Siri mode error: {e}")
            
            elif user_input in ['6', 'wake', 'wake word', 'hey jarvis']:
                print("[MODE] Wake word mode - Say 'Hey Jarvis'")
                speak("Entering wake word mode. Say Hey Jarvis to activate")
                wake_word_mode()
            
            elif user_input in ['7', 'agent', 'smart', 'multi-step', 'smart agent']:
                print("[MODE] Smart agent mode - Multi-step task execution")
                speak("Entering smart agent mode")
                smart_agent_mode()
            
            elif user_input in ['8', 'help', 'show', 'commands']:
                from voice.listen import voice_command_reference
                voice_command_reference()
            
            elif user_input in ['9', 'settings', 'config', 'preferences']:
                settings_menu()
            
            elif user_input in ['10', 'exit', 'quit', 'stop', 'goodbye']:
                speak("Shutting down. Goodbye!")
                break
            
            else:
                # User typed a command
                response = execute(user_input)
                if response:
                    print(f"[RESPONSE] {response}")
                    speak(response)
                    # Save to memory
                    save_memory(user_input, response)
    
    except KeyboardInterrupt:
        print("\n\n[!] Keyboard interrupt detected")
        speak("Shutting down")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        speak("An error occurred. Please try again.")
    finally:
        cleanup_wake_word()

def text_mode_loop():
    """Continuous text command mode"""
    print("[COMMANDS] Type commands or 'back' to return to menu:\n")
    
    exit_main = False
    
    while True:
        print("[COMMAND] ", end="")
        command = input().strip().lower()
        
        if command in ['back', 'menu', 'exit text']:
            print("[EXIT] Returning to main menu")
            break
        
        if not command:
            continue
        
        if command in ['exit', 'quit', 'stop']:
            speak("Shutting down. Goodbye!")
            exit_main = True
            break
        
        response = execute(command)
        if response:
            print(f"[RESPONSE] {response}\n")
            speak(response)
            save_memory(command, response)
    
    return exit_main


def wake_word_mode():
    """Wake word detection mode - always listening for 'Hey Jarvis'"""
    print("\n[WAKE WORD MODE]")
    print("Listening for 'Hey Jarvis'...")
    print("Press Ctrl+C to exit\n")
    
    speak("Wake word mode active. Say Hey Jarvis to activate")
    
    try:
        while True:
            # Listen for wake word
            if detect_wake_word():
                print("\n🔥 WAKE WORD DETECTED!")
                speak("I'm listening. What do you need?")
                
                # Listen for command
                from voice.listen import listen_with_retry
                command = listen_with_retry(max_retries=2)
                
                if command:
                    print(f"[COMMAND] {command}")
                    
                    # Try smart agent first for complex tasks
                    if any(keyword in command.lower() for keyword in ['prepare', 'generate', 'create', 'build', 'analyze', 'automate']):
                        response = execute_smart_task(command)
                    else:
                        response = execute(command)
                    
                    if response:
                        print(f"[RESPONSE] {response}")
                        speak(response)
                        save_memory(command, response)
                    
                    print("\nListening for next command...")
    
    except KeyboardInterrupt:
        print("\n[EXIT] Wake word mode stopped")
        speak("Wake word mode deactivated")
    except Exception as e:
        print(f"[ERROR] {e}")
        speak(f"Error: {e}")


def smart_agent_mode():
    """Smart agent mode - multi-step task execution"""
    print("\n[SMART AGENT MODE]")
    print("Describe your multi-step task or type 'back' to return:\n")
    
    speak("Smart agent mode activated. Describe your task")
    
    try:
        while True:
            print("[TASK] ", end="")
            task = input().strip()
            
            if task.lower() in ['back', 'menu', 'exit']:
                speak("Exiting smart agent mode")
                break
            
            if not task:
                continue
            
            print(f"\n🤖 Processing: {task}")
            speak("Processing your task. This may take a moment.")
            
            # Execute with smart agent
            response = execute_smart_task(task)
            
            print(f"[RESULT] {response}\n")
            speak(response)
            save_memory(task, response, memory_type="agent_task")
            
            print("\nReady for next task...")
    
    except KeyboardInterrupt:
        print("\n[EXIT] Smart agent mode stopped")
        speak("Smart agent mode deactivated")
    except Exception as e:
        print(f"[ERROR] {e}")
        speak(f"Error: {e}")


def settings_menu():
    """Settings and preferences menu"""
    print("\n[SETTINGS]")
    print("   1. Show user preferences")
    print("   2. Clear memory")
    print("   3. Install background service")
    print("   4. Uninstall background service")
    print("   5. View memory stats")
    print("   6. Back to main menu")
    print()
    
    choice = input("Choose option: ").strip().lower()
    
    if choice in ['1', 'preferences', 'show']:
        print("\n[USER PREFERENCES]")
        prefs = get_user_preferences()
        if prefs:
            for key, value in prefs.items():
                print(f"   {key}: {value}")
        else:
            print("   No preferences learned yet")
            speak("No preferences learned yet")
    
    elif choice in ['2', 'clear', 'memory']:
        confirm = input("Clear all memory? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            from brain.memory import get_memory
            get_memory().clear_memory()
            speak("Memory cleared")
            print("✅ Memory cleared")
    
    elif choice in ['3', 'install', 'service']:
        from service_runner import install_service
        if install_service():
            speak("Service installed successfully")
            print("✅ Service installed. Jarvis will start automatically on boot")
        else:
            speak("Installation failed")
            print("❌ Installation failed")
    
    elif choice in ['4', 'uninstall', 'remove']:
        confirm = input("Uninstall service? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            from service_runner import uninstall_service
            if uninstall_service():
                speak("Service uninstalled successfully")
                print("✅ Service uninstalled")
            else:
                speak("Uninstall failed")
                print("❌ Uninstall failed")
    
    elif choice in ['5', 'stats', 'info']:
        from brain.memory import get_memory
        memory = get_memory()
        print("[MEMORY STATS]")
        print(f"   Collection: {memory.collection.count()} items")
        speak(f"Memory contains {memory.collection.count()} items")
    
    print()

def main():
    """Main entry point"""
    print("\n[>>] Starting Jarvis AI Assistant...\n")
    
    # Display welcome message
    display_welcome()
    
    # Start main loop
    try:
        jarvis_loop()
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")
        speak("Fatal error occurred")
    
    print("\n[OK] Jarvis has been shut down.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
