"""
Background Service Runner - Run Jarvis as always-on daemon
Enables system startup integration and persistent listening
"""

import os
import sys
import signal
import time
import subprocess
from pathlib import Path
from config import DEBUG_MODE


class JarvisService:
    """Background service runner for Jarvis"""
    
    def __init__(self):
        """Initialize service"""
        self.is_running = False
        self.pid = os.getpid()
        
        # Project root directory
        self.project_root = Path(__file__).parent
        self.pid_file = self.project_root / ".jarvis.pid"
        self.log_file = self.project_root / "jarvis_service.log"
    
    def start(self):
        """Start Jarvis service"""
        try:
            self.is_running = True
            
            # Write PID file
            with open(self.pid_file, 'w') as f:
                f.write(str(self.pid))
            
            # Log startup
            self._log(f"🚀 Jarvis service started (PID: {self.pid})")
            
            # Import and start main loop
            from main import jarvis_loop
            
            # Handle interrupts gracefully
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # Run main loop
            jarvis_loop()
        
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            self._log(f"❌ Service error: {e}")
            self.stop()
    
    def stop(self):
        """Stop service cleanly"""
        try:
            self.is_running = False
            
            # Clean up PID file
            if self.pid_file.exists():
                self.pid_file.unlink()
            
            self._log("⏹️  Jarvis service stopped")
            sys.exit(0)
        
        except Exception as e:
            self._log(f"❌ Stop error: {e}")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals"""
        self._log(f"📢 Received signal {signum}")
        self.stop()
    
    def _log(self, message):
        """Log to file and console"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_message + "\n")
        except:
            pass


def create_startup_task():
    """Create Windows startup task"""
    try:
        import winreg
        
        project_root = Path(__file__).parent
        python_exe = sys.executable
        script_path = project_root / "service_runner.py"
        
        # Registry path for startup
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        # Create registry entry
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            reg_path,
            0,
            winreg.KEY_WRITE
        )
        
        command = f'"{python_exe}" "{script_path}"'
        winreg.SetValueEx(
            registry_key,
            "JarvisAI",
            0,
            winreg.REG_SZ,
            command
        )
        
        winreg.CloseKey(registry_key)
        
        if DEBUG_MODE:
            print("✅ Startup task created")
        
        return True
    
    except Exception as e:
        if DEBUG_MODE:
            print(f"❌ Startup task error: {e}")
        return False


def remove_startup_task():
    """Remove Windows startup task"""
    try:
        import winreg
        
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            reg_path,
            0,
            winreg.KEY_WRITE
        )
        
        try:
            winreg.DeleteValue(registry_key, "JarvisAI")
        except:
            pass
        
        winreg.CloseKey(registry_key)
        
        if DEBUG_MODE:
            print("✅ Startup task removed")
        
        return True
    
    except Exception as e:
        if DEBUG_MODE:
            print(f"❌ Remove startup error: {e}")
        return False


def install_service():
    """Install Jarvis as background service"""
    try:
        if DEBUG_MODE:
            print("📦 Installing Jarvis service...")
        
        project_root = Path(__file__).parent
        
        # Create batch file for startup
        batch_file = project_root / "run_jarvis_service.bat"
        python_exe = sys.executable
        
        batch_content = f"""@echo off
cd /d "{project_root}"
"{python_exe}" -m service_runner
"""
        
        with open(batch_file, 'w') as f:
            f.write(batch_content)
        
        # Create startup task
        create_startup_task()
        
        if DEBUG_MODE:
            print("✅ Service installed successfully")
        
        return True
    
    except Exception as e:
        if DEBUG_MODE:
            print(f"❌ Installation error: {e}")
        return False


def uninstall_service():
    """Uninstall Jarvis service"""
    try:
        if DEBUG_MODE:
            print("🗑️  Uninstalling Jarvis service...")
        
        remove_startup_task()
        
        project_root = Path(__file__).parent
        batch_file = project_root / "run_jarvis_service.bat"
        
        if batch_file.exists():
            batch_file.unlink()
        
        if DEBUG_MODE:
            print("✅ Service uninstalled successfully")
        
        return True
    
    except Exception as e:
        if DEBUG_MODE:
            print(f"❌ Uninstall error: {e}")
        return False


if __name__ == "__main__":
    """Main entry point for service runner"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "install":
            install_service()
        elif command == "uninstall":
            uninstall_service()
        else:
            print("Usage: service_runner.py [install|uninstall]")
    else:
        # Run as service
        service = JarvisService()
        service.start()
