# Advanced System Control Module - Full computer automation

import pyautogui
import time
import subprocess
import os
import shutil
import psutil
import json
from datetime import datetime
from config import DEBUG_MODE

# ========== APPLICATION LAUNCHING ==========

def open_app(app_name):
    """Open any application by name"""
    try:
        if DEBUG_MODE:
            print(f"🚀 Opening {app_name}...")
        
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write(app_name, interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")
        
        return f"Opening {app_name}"
    except Exception as e:
        return f"Error opening {app_name}: {e}"

def open_chrome():
    """Open Google Chrome browser"""
    return open_app("chrome")

def open_notepad():
    """Open Notepad text editor"""
    return open_app("notepad")

def open_calculator():
    """Open Calculator application"""
    return open_app("calculator")

def open_vscode():
    """Open Visual Studio Code"""
    return open_app("code")

def open_file(file_path):
    """Open any file with default application"""
    try:
        if DEBUG_MODE:
            print(f"📄 Opening file: {file_path}")
        
        if os.path.exists(file_path):
            os.startfile(file_path)
            return f"Opening {os.path.basename(file_path)}"
        else:
            return f"File not found: {file_path}"
    except Exception as e:
        return f"Error opening file: {e}"

def open_folder(folder_path):
    """Open folder in File Explorer"""
    try:
        if DEBUG_MODE:
            print(f"📁 Opening folder: {folder_path}")
        
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')
            return f"Opening folder: {folder_path}"
        else:
            return f"Folder not found: {folder_path}"
    except Exception as e:
        return f"Error opening folder: {e}"

# ========== FILE MANAGEMENT ==========

def create_file(file_path, content=""):
    """Create a new file with content"""
    try:
        if DEBUG_MODE:
            print(f"✍️ Creating file: {file_path}")
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Created file: {file_path}"
    except Exception as e:
        return f"Error creating file: {e}"

def delete_file(file_path):
    """Delete a file"""
    try:
        if DEBUG_MODE:
            print(f"🗑️ Deleting file: {file_path}")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"Deleted file: {file_path}"
        else:
            return f"File not found: {file_path}"
    except Exception as e:
        return f"Error deleting file: {e}"

def copy_file(source, destination):
    """Copy a file"""
    try:
        if DEBUG_MODE:
            print(f"📋 Copying: {source} → {destination}")
        
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy2(source, destination)
        return f"Copied to: {destination}"
    except Exception as e:
        return f"Error copying file: {e}"

def move_file(source, destination):
    """Move/cut a file"""
    try:
        if DEBUG_MODE:
            print(f"📦 Moving: {source} → {destination}")
        
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)
        return f"Moved to: {destination}"
    except Exception as e:
        return f"Error moving file: {e}"

def list_files(directory):
    """List all files in a directory"""
    try:
        if DEBUG_MODE:
            print(f"📂 Listing files in: {directory}")
        
        if os.path.exists(directory):
            files = os.listdir(directory)
            return f"Files in {directory}:\n" + "\n".join(files[:20])
        else:
            return f"Directory not found: {directory}"
    except Exception as e:
        return f"Error listing files: {e}"

# ========== WINDOW MANAGEMENT ==========

def minimize_all():
    """Minimize all windows"""
    try:
        if DEBUG_MODE:
            print("➖ Minimizing all windows...")
        
        pyautogui.hotkey("win", "d")
        return "All windows minimized"
    except Exception as e:
        return f"Error minimizing windows: {e}"

def maximize_window():
    """Maximize current window"""
    try:
        if DEBUG_MODE:
            print("⬆️ Maximizing window...")
        
        pyautogui.hotkey("win", "Up")
        return "Window maximized"
    except Exception as e:
        return f"Error maximizing window: {e}"

def close_window():
    """Close current window"""
    try:
        if DEBUG_MODE:
            print("❌ Closing window...")
        
        pyautogui.hotkey("alt", "F4")
        return "Window closed"
    except Exception as e:
        return f"Error closing window: {e}"

# ========== KEYBOARD & MOUSE CONTROL ==========

def type_text(text):
    """Type text automatically"""
    try:
        if DEBUG_MODE:
            print(f"⌨️ Typing: {text}")
        
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"
    except Exception as e:
        return f"Error typing: {e}"

def click_mouse(x, y):
    """Click mouse at coordinates"""
    try:
        if DEBUG_MODE:
            print(f"🖱️ Clicking at ({x}, {y})...")
        
        pyautogui.click(x, y)
        return f"Clicked at ({x}, {y})"
    except Exception as e:
        return f"Error clicking: {e}"

def move_mouse(x, y):
    """Move mouse to coordinates"""
    try:
        if DEBUG_MODE:
            print(f"🖱️ Moving mouse to ({x}, {y})...")
        
        pyautogui.moveTo(x, y)
        return f"Mouse moved to ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse: {e}"

def press_key(key):
    """Press a keyboard key"""
    try:
        if DEBUG_MODE:
            print(f"⌨️ Pressing: {key}")
        
        pyautogui.press(key)
        return f"Pressed: {key}"
    except Exception as e:
        return f"Error pressing key: {e}"

def hotkey(modifier, key):
    """Press key combination (Ctrl+C, Alt+Tab, etc)"""
    try:
        if DEBUG_MODE:
            print(f"⌨️ Hotkey: {modifier}+{key}")
        
        pyautogui.hotkey(modifier, key)
        return f"Executed: {modifier}+{key}"
    except Exception as e:
        return f"Error with hotkey: {e}"

# ========== SCREENSHOT & CAPTURE ==========

def take_screenshot(save_path="screenshot.png"):
    """Take a screenshot"""
    try:
        if DEBUG_MODE:
            print(f"📸 Taking screenshot...")
        
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return f"Screenshot saved: {save_path}"
    except Exception as e:
        return f"Error taking screenshot: {e}"

# ========== CLIPBOARD MANAGEMENT ==========

def copy_to_clipboard(text):
    """Copy text to clipboard"""
    try:
        if DEBUG_MODE:
            print(f"📋 Copying to clipboard...")
        
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("delete")
        pyautogui.write(text, interval=0.01)
        pyautogui.hotkey("ctrl", "c")
        return f"Copied to clipboard: {text[:50]}"
    except Exception as e:
        return f"Error copying: {e}"

# ========== PROCESS MANAGEMENT ==========

def get_running_apps():
    """Get list of running applications"""
    try:
        if DEBUG_MODE:
            print("📋 Getting running apps...")
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                processes.append(proc.info['name'])
            except psutil.NoSuchProcess:
                pass
        
        return f"Running applications:\n" + "\n".join(processes[:20])
    except Exception as e:
        return f"Error getting processes: {e}"

def kill_process(process_name):
    """Kill a running process"""
    try:
        if DEBUG_MODE:
            print(f"🛑 Killing process: {process_name}")
        
        subprocess.run(["taskkill", "/IM", process_name, "/F"], check=True)
        return f"Killed process: {process_name}"
    except Exception as e:
        return f"Error killing process: {e}"

# ========== SCREEN CONTROL ==========

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
        
        subprocess.run(["shutdown", "/s", "/t", "30"], check=True)
        return "Computer will shutdown in 30 seconds"
    except Exception as e:
        return f"Error during shutdown: {e}"

def restart_computer():
    """Restart the computer"""
    try:
        if DEBUG_MODE:
            print("🔄 Restarting...")
        
        subprocess.run(["shutdown", "/r", "/t", "30"], check=True)
        return "Computer will restart in 30 seconds"
    except Exception as e:
        return f"Error during restart: {e}"

def hibernate():
    """Put computer to sleep/hibernate"""
    try:
        if DEBUG_MODE:
            print("😴 Hibernating...")
        
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"], check=True)
        return "Computer entering hibernation"
    except Exception as e:
        return f"Error hibernating: {e}"

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

def mute_sound():
    """Mute system audio"""
    try:
        pyautogui.press("volumemute")
        return "Sound muted"
    except Exception as e:
        return f"Error muting sound: {e}"

# ========== NETWORK CONTROL ==========

def check_internet():
    """Check if connected to internet"""
    try:
        if DEBUG_MODE:
            print("🌐 Checking internet connection...")
        
        import socket
        socket.create_connection(("8.8.8.8", 53))
        return "✅ Internet connection active"
    except:
        return "❌ No internet connection"

def get_wifi_info():
    """Get WiFi information"""
    try:
        if DEBUG_MODE:
            print("📡 Getting WiFi info...")
        
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error getting WiFi info: {e}"

# ========== SYSTEM INFORMATION ==========

def get_system_performance():
    """Get CPU, RAM, Disk usage"""
    try:
        if DEBUG_MODE:
            print("📊 Getting system performance...")
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"""
📊 SYSTEM PERFORMANCE
CPU Usage: {cpu_percent}%
RAM Usage: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
Disk: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
        """
        return info
    except Exception as e:
        return f"Error getting performance: {e}"

def get_battery_status():
    """Get battery information"""
    try:
        if DEBUG_MODE:
            print("🔋 Getting battery status...")
        
        battery = psutil.sensors_battery()
        if battery:
            return f"🔋 Battery: {battery.percent}% - {'Charging' if battery.power_plugged else 'Discharging'}"
        else:
            return "No battery found (Desktop)"
    except Exception as e:
        return f"Error getting battery: {e}"
