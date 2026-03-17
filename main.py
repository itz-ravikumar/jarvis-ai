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
    print("\n" + "="*70)
    print(f"[AI] Welcome to {ASSISTANT_NAME} AI Assistant - PRODUCTION v4.0")
    print("="*70)
    print("[MAIN MENU - Core Features]")
    print("   1. Text commands (type commands)")
    print("   2. Voice mode (interactive menu)")
    print("   3. Quick voice (single command)")
    print("   4. Conversation mode (back & forth talking) ⭐")
    print("   5. Always-listening mode (Siri-like)")
    print("   6. Wake word mode (Say 'Hey Jarvis') 🔥")
    print("   7. Smart agent mode (multi-step tasks)")
    print("\n[PRODUCTION FEATURES - NEW!] 🚀")
    print("   11. Continuous hands-free mode (Siri-level)")
    print("   12. Hybrid smart execution (AI + commands)")
    print("   13. REST API server (control from mobile)")
    print("   14. Telegram bot interface (control from phone)")
    print("   15. Start background service (auto-start)")
    print("   16. Floating GUI (Siri-style window)")
    print("\n[UTILITIES]")
    print("   8. Show all commands")
    print("   9. Show memory/preferences")
    print("   10. Settings")
    print("   0. Exit")
    print("="*70)
    print("\n[PRODUCTION STATUS]")
    print("   ✅ AI Intelligence - Groq enabled")
    print("   ✅ Wake word detection - 'Hey Jarvis'")
    print("   ✅ Continuous listening - Hands-free flow")
    print("   ✅ Memory system - Context aware")
    print("   ✅ Smart agent - Multi-step automation")
    print("   ✅ Cross-device - Mobile integration")
    print("   ✅ Background service - Always running")
    print("="*70 + "\n")

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
            
            # ========== PRODUCTION FEATURES ==========
            elif user_input in ['11', 'continuous', 'continuous mode', 'hands-free']:
                print("[MODE] Continuous hands-free listening (Siri-style)")
                speak("Entering continuous listening mode. Say hey Jarvis to activate")
                continuous_hands_free_mode()
            
            elif user_input in ['12', 'hybrid', 'smart execution']:
                print("[MODE] Hybrid smart execution")
                speak("Entering hybrid mode with intelligent task routing")
                hybrid_smart_mode()
            
            elif user_input in ['13', 'api', 'api server', 'rest']:
                print("[MODE] REST API Server for mobile control")
                speak("Starting API server on port 5000")
                api_server_mode()
            
            elif user_input in ['14', 'telegram', 'telegram bot']:
                print("[MODE] Telegram bot interface")
                speak("Starting Telegram bot")
                telegram_mode()
            
            elif user_input in ['15', 'service', 'background', 'auto-start']:
                print("[MODE] Background service setup")
                speak("Setting up background service")
                install_background_service()
            
            elif user_input in ['16', 'gui', 'floating', 'window']:
                print("[MODE] Floating Siri-style GUI")
                speak("Starting floating window")
                floating_gui_mode()
            
            # ========== UTILITIES ==========
            elif user_input in ['8', 'help', 'show', 'commands']:
                from voice.listen import voice_command_reference
                voice_command_reference()
            
            elif user_input in ['9', 'memory', 'preferences', 'recall']:
                print("[MEMORY] Your saved preferences:")
                prefs = get_user_preferences()
                for key, value in prefs.items():
                    print(f"  • {key}: {value}")
            
            elif user_input in ['10', 'settings', 'config', 'preferences']:
                settings_menu()
            
            elif user_input in ['0', 'exit', 'quit', 'stop', 'goodbye']:
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


# ========== PRODUCTION MODE HANDLERS ==========

def continuous_hands_free_mode():
    """Continuous Siri-style hands-free listening"""
    try:
        from voice.continuous_mode import continuous_wake_word_mode
        continuous_wake_word_mode()
    except ImportError:
        print("[ERROR] Continuous mode not available")
        speak("Continuous mode not available")
    except Exception as e:
        print(f"[ERROR] {e}")
        speak(f"Error: {e}")


def hybrid_smart_mode():
    """Hybrid execution with intelligent routing"""
    try:
        from voice.continuous_mode import smart_hybrid_mode
        smart_hybrid_mode()
    except ImportError:
        print("[ERROR] Hybrid mode not available")
        speak("Hybrid mode not available")
    except Exception as e:
        print(f"[ERROR] {e}")
        speak(f"Error: {e}")


def api_server_mode():
    """REST API server for mobile control"""
    try:
        from integrations.cross_device import setup_cross_device
        setup_cross_device(mode="api", host="0.0.0.0", port=5000)
    except ImportError:
        print("[ERROR] REST API not available. Install: pip install fastapi uvicorn")
        speak("API server not available")
    except Exception as e:
        print(f"[ERROR] {e}")
        speak(f"Error: {e}")


def telegram_mode():
    """Telegram bot interface for mobile control"""
    try:
        token = input("[INPUT] Enter your Telegram Bot Token: ").strip()
        if not token:
            speak("Token required for Telegram bot")
            return
        
        from integrations.cross_device import telegram_bot_server
        telegram_bot_server(token)
    except ImportError:
        print("[ERROR] Telegram bot not available. Install: pip install pyTelegramBotAPI")
        speak("Telegram bot not available")
    except Exception as e:
        print(f"[ERROR] {e}")
        speak(f"Error: {e}")


def install_background_service():
    """Install background service for auto-start"""
    try:
        from service_runner import install_service
        if install_service():
            speak("Background service installed successfully")
            print("[OK] Service installed. Jarvis will auto-start on boot.")
        else:
            speak("Service installation failed")
            print("[ERROR] Service installation failed")
    except Exception as e:
        print(f"[ERROR] {e}")
        speak(f"Error: {e}")


def floating_gui_mode():
    """Start floating Siri-style GUI"""
    try:
        print("[INFO] Checking for PyQt5...")
        
        try:
            from ui.floating_window import start_floating_ui
            ui = start_floating_ui()
            speak("Floating GUI started")
            print("[OK] Floating window started. Commands from here now...")
            
            # Keep listening
            while True:
                pass
        
        except ImportError:
            print("[INFO] PyQt5 not installed. Starting terminal UI instead...")
            from ui.floating_window import SimpleFloatingUI
            ui = SimpleFloatingUI()
            speak("Starting terminal interface")
            
            while True:
                cmd = input("[COMMAND] ").strip()
                if cmd.lower() in ['exit', 'stop']:
                    break
                
                response = execute(cmd)
                if response:
                    ui.update_state("speaking")
                    speak(response)
                    ui.update_state("ready")
    
    except KeyboardInterrupt:
        print("\n[EXIT] Floating GUI closed")
        speak("GUI closed")
    except Exception as e:
        print(f"[ERROR] {e}")
        speak(f"Error: {e}")

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
