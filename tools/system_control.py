# System Control Module - Controls computer applications and OS

import pyautogui
import time
from config import DEBUG_MODE

def open_chrome():
    """Open Google Chrome browser"""
    try:
        if DEBUG_MODE:
            print("🚀 Opening Chrome...")
        
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write("chrome", interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")
        
        return "Opening Chrome"
    except Exception as e:
        return f"Error opening Chrome: {e}"

def open_notepad():
    """Open Notepad text editor"""
    try:
        if DEBUG_MODE:
            print("🚀 Opening Notepad...")
        
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write("notepad", interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")
        
        return "Opening Notepad"
    except Exception as e:
        return f"Error opening Notepad: {e}"

def open_calculator():
    """Open Calculator application"""
    try:
        if DEBUG_MODE:
            print("🚀 Opening Calculator...")
        
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write("calculator", interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")
        
        return "Opening Calculator"
    except Exception as e:
        return f"Error opening Calculator: {e}"

def open_vscode():
    """Open Visual Studio Code"""
    try:
        if DEBUG_MODE:
            print("🚀 Opening VS Code...")
        
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write("code", interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")
        
        return "Opening Visual Studio Code"
    except Exception as e:
        return f"Error opening VS Code: {e}"

def lock_screen():
    """Lock the Windows screen"""
    try:
        if DEBUG_MODE:
            print("🔒 Locking screen...")
        
        pyautogui.hotkey("win", "l")
        
        return "Screen locked"
    except Exception as e:
        return f"Error locking screen: {e}"

def shutdown_computer():
    """Shutdown the computer"""
    try:
        if DEBUG_MODE:
            print("🛑 Shutting down...")
        
        import subprocess
        subprocess.run(["shutdown", "/s", "/t", "30"], check=True)
        
        return "Computer will shutdown in 30 seconds"
    except Exception as e:
        return f"Error during shutdown: {e}"

def volume_up():
    """Increase system volume"""
    try:
        pyautogui.press("volumeup")
        return "Volume increased"
    except Exception as e:
        return f"Error adjusting volume: {e}"

def volume_down():
    """Decrease system volume"""
    try:
        pyautogui.press("volumedown")
        return "Volume decreased"
    except Exception as e:
        return f"Error adjusting volume: {e}"
