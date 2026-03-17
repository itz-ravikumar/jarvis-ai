"""
Advanced Command Executor - Execute real system commands
Handles: apps, files, web, keyboard, mouse, scripts
"""

import os
import subprocess
import sys
import time
from pathlib import Path
from config import DEBUG_MODE

class AdvancedExecutor:
    """Execute commands on the system"""
    
    def __init__(self):
        """Initialize executor"""
        self.commands = {
            # App control
            'open': self.open_app,
            'close': self.close_app,
            'launch': self.open_app,
            'start': self.open_app,
            
            # File operations
            'create': self.create_file,
            'delete': self.delete_file,
            'copy': self.copy_file,
            'move': self.move_file,
            'list': self.list_files,
            'show': self.list_files,
            'read': self.read_file,
            
            # System commands
            'shutdown': self.shutdown,
            'restart': self.restart,
            'sleep': self.sleep_system,
            'lock': self.lock_screen,
            
            # Keyboard/Mouse (advanced)
            'type': self.keyboard_type,
            'click': self.mouse_click,
            'press': self.key_press,
            
            # Browser
            'search': self.web_search,
            'google': self.web_search,
            'visit': self.open_website,
            
            # System info
            'time': self.get_time,
            'date': self.get_date,
            'weather': self.get_weather,
        }
    
    def execute(self, command: str) -> str:
        """Execute any command"""
        try:
            command_lower = command.lower().strip()
            
            # Find matching command
            for keyword, func in self.commands.items():
                if keyword in command_lower:
                    result = func(command)
                    return result
            
            # Fallback: try as system command
            return self.run_system_command(command)
        
        except Exception as e:
            return f"Error: {e}"
    
    # ========== APP CONTROL ==========
    
    def open_app(self, command: str) -> str:
        """Open application"""
        try:
            app_map = {
                'chrome': 'chrome',
                'firefox': 'firefox',
                'notepad': 'notepad',
                'word': 'winword',
                'excel': 'excel',
                'powerpoint': 'powerpnt',
                'vscode': 'code',
                'vs code': 'code',
                'calculator': 'calc',
                'notepad++': 'notepad++',
                'git': 'git',
                'python': 'python',
                'cmd': 'cmd',
                'powershell': 'powershell',
                'slack': 'slack',
                'teams': 'teams',
                'discord': 'discord',
                'spotify': 'spotify',
                'edge': 'msedge',
            }
            
            # Extract app name
            for app_name, exe_name in app_map.items():
                if app_name in command.lower():
                    try:
                        subprocess.Popen(exe_name)
                        if DEBUG_MODE:
                            print(f"✅ Opened {app_name}")
                        return f"Opening {app_name}..."
                    except:
                        return f"{app_name} not found on system"
            
            return "App not recognized. Try: Chrome, Firefox, Notepad, Word, Excel, VSCode, Discord, Slack"
        
        except Exception as e:
            return f"Error opening app: {e}"
    
    def close_app(self, command: str) -> str:
        """Close application"""
        try:
            app_name = command.replace('close', '').replace('quit', '').strip()
            
            if 'chrome' in app_name.lower():
                os.system('taskkill /IM chrome.exe /F')
                return "Chrome closed"
            elif 'firefox' in app_name.lower():
                os.system('taskkill /IM firefox.exe /F')
                return "Firefox closed"
            elif 'notepad' in app_name.lower():
                os.system('taskkill /IM notepad.exe /F')
                return "Notepad closed"
            else:
                os.system(f'taskkill /IM {app_name}.exe /F')
                return f"{app_name} closed"
        
        except Exception as e:
            return f"Error: {e}"
    
    # ========== FILE OPERATIONS ==========
    
    def create_file(self, command: str) -> str:
        """Create new file"""
        try:
            filename = command.replace('create', '').replace('file', '').strip()
            
            if not filename:
                return "Specify filename: 'create notes.txt'"
            
            filepath = Path(filename)
            filepath.touch()
            
            if DEBUG_MODE:
                print(f"✅ Created {filepath}")
            return f"File '{filename}' created"
        
        except Exception as e:
            return f"Error: {e}"
    
    def delete_file(self, command: str) -> str:
        """Delete file"""
        try:
            filename = command.replace('delete', '').strip()
            
            if not filename:
                return "Specify filename: 'delete notes.txt'"
            
            if os.path.exists(filename):
                os.remove(filename)
                return f"File '{filename}' deleted"
            else:
                return f"File not found: {filename}"
        
        except Exception as e:
            return f"Error: {e}"
    
    def copy_file(self, command: str) -> str:
        """Copy file"""
        try:
            parts = command.replace('copy', '').split('to')
            if len(parts) != 2:
                return "Syntax: 'copy source.txt to destination.txt'"
            
            source = parts[0].strip()
            dest = parts[1].strip()
            
            import shutil
            shutil.copy(source, dest)
            return f"Copied '{source}' to '{dest}'"
        
        except Exception as e:
            return f"Error: {e}"
    
    def move_file(self, command: str) -> str:
        """Move/rename file"""
        try:
            parts = command.replace('move', '').split('to')
            if len(parts) != 2:
                return "Syntax: 'move old.txt to new.txt'"
            
            source = parts[0].strip()
            dest = parts[1].strip()
            
            os.rename(source, dest)
            return f"Moved '{source}' to '{dest}'"
        
        except Exception as e:
            return f"Error: {e}"
    
    def list_files(self, command: str) -> str:
        """List files in directory"""
        try:
            path = command.replace('list', '').replace('show', '').replace('files', '').strip() or '.'
            
            if not os.path.exists(path):
                return f"Path not found: {path}"
            
            files = os.listdir(path)
            result = f"Files in {path}:\n"
            for i, file in enumerate(files[:10], 1):  # Show first 10
                result += f"{i}. {file}\n"
            
            if len(files) > 10:
                result += f"... and {len(files)-10} more"
            
            return result
        
        except Exception as e:
            return f"Error: {e}"
    
    def read_file(self, command: str) -> str:
        """Read file content"""
        try:
            filename = command.replace('read', '').strip()
            
            if not filename:
                return "Specify filename: 'read notes.txt'"
            
            with open(filename, 'r') as f:
                content = f.read()
            
            return f"Content of '{filename}':\n{content[:500]}"  # First 500 chars
        
        except Exception as e:
            return f"Error: {e}"
    
    # ========== SYSTEM COMMANDS ==========
    
    def shutdown(self, command: str) -> str:
        """Shutdown computer"""
        try:
            delay = 30  # 30 seconds delay
            
            # Check if custom delay specified
            if 'in' in command:
                try:
                    delay = int(command.split('in')[1].split()[0])
                except:
                    pass
            
            if delay > 0:
                result = f"System will shutdown in {delay} seconds. Cancel with: 'cancel shutdown'"
                subprocess.call(f'shutdown /s /t {delay}')
                return result
            else:
                subprocess.call('shutdown /s /t 0')
                return "System shutting down now"
        
        except Exception as e:
            return f"Error: {e}"
    
    def restart(self, command: str) -> str:
        """Restart computer"""
        try:
            delay = 30
            if 'in' in command:
                try:
                    delay = int(command.split('in')[1].split()[0])
                except:
                    pass
            
            subprocess.call(f'shutdown /r /t {delay}')
            return f"System will restart in {delay} seconds"
        
        except Exception as e:
            return f"Error: {e}"
    
    def sleep_system(self, command: str) -> str:
        """Put system to sleep"""
        try:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            return "System sleeping"
        except:
            return "Error putting system to sleep"
    
    def lock_screen(self, command: str) -> str:
        """Lock screen"""
        try:
            os.system('rundll32.exe user32.dll,LockWorkStation')
            return "Screen locked"
        except:
            return "Error locking screen"
    
    # ========== KEYBOARD/MOUSE (Advanced) ==========
    
    def keyboard_type(self, command: str) -> str:
        """Type text via keyboard"""
        try:
            text = command.replace('type', '').strip()
            
            try:
                import pyautogui
                pyautogui.typewrite(text)
                return f"Typed: {text}"
            except:
                return "PyAutoGUI not available"
        
        except Exception as e:
            return f"Error: {e}"
    
    def mouse_click(self, command: str) -> str:
        """Click mouse at position"""
        try:
            try:
                import pyautogui
                
                if 'left' in command:
                    pyautogui.click(button='left')
                elif 'right' in command:
                    pyautogui.click(button='right')
                else:
                    pyautogui.click()
                
                return "Mouse clicked"
            except:
                return "PyAutoGUI not available"
        
        except Exception as e:
            return f"Error: {e}"
    
    def key_press(self, command: str) -> str:
        """Press keyboard key"""
        try:
            try:
                import pyautogui
                
                key = command.replace('press', '').strip().lower()
                pyautogui.press(key)
                return f"Pressed: {key}"
            except:
                return "PyAutoGUI not available"
        
        except Exception as e:
            return f"Error: {e}"
    
    # ========== WEB OPERATIONS ==========
    
    def web_search(self, command: str) -> str:
        """Search the web"""
        try:
            query = command.replace('search', '').replace('google', '').strip()
            
            try:
                from langchain_community.tools import DuckDuckGoSearchRun
                search = DuckDuckGoSearchRun()
                result = search.run(query)
                return result
            except:
                # Fallback: open in browser
                import webbrowser
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return f"Searching: {query}"
        
        except Exception as e:
            return f"Error: {e}"
    
    def open_website(self, command: str) -> str:
        """Open website in browser"""
        try:
            url = command.replace('visit', '').replace('go to', '').strip()
            
            if not url.startswith('http'):
                url = f"https://{url}"
            
            import webbrowser
            webbrowser.open(url)
            return f"Opening: {url}"
        
        except Exception as e:
            return f"Error: {e}"
    
    # ========== SYSTEM INFO ==========
    
    def get_time(self, command: str) -> str:
        """Get current time"""
        from datetime import datetime
        return f"Current time: {datetime.now().strftime('%H:%M:%S')}"
    
    def get_date(self, command: str) -> str:
        """Get current date"""
        from datetime import datetime
        return f"Current date: {datetime.now().strftime('%A, %B %d, %Y')}"
    
    def get_weather(self, command: str) -> str:
        """Get weather (placeholder)"""
        return "Weather feature requires API key. Configure in settings."
    
    # ========== FALLBACK ==========
    
    def run_system_command(self, command: str) -> str:
        """Run as system command"""
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except:
            return f"Command not recognized: {command}"


# Global executor
_executor = None

def get_executor():
    """Get global executor instance"""
    global _executor
    if _executor is None:
        _executor = AdvancedExecutor()
    return _executor


def execute_advanced(command: str) -> str:
    """Execute command with advanced executor"""
    executor = get_executor()
    return executor.execute(command)
