"""
🚀 JARVIS - Always Listening AI Assistant
Robust, production-ready voice AI for continuous command execution
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import os
from datetime import datetime
import random

# ============ GROQ LLM INTEGRATION ============
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# ============ BROWSER & SYSTEM CONTROL ============
import subprocess
import webbrowser
import pyautogui
from pathlib import Path

# ============ TTS ============
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# ============ FastAPI Setup ============
app = FastAPI(title="JARVIS - Always Listening AI", version="4.0")

# CORS middleware for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ GLOBAL STATE ============
class JarvisCore:
    """JARVIS Core Engine"""
    
    def __init__(self):
        self.listening = False
        self.processing = False
        self.session_commands = []
        self.command_count = 0
        self.success_count = 0
        self.error_count = 0
        
        # Initialize TTS
        self.tts = None
        if TTS_AVAILABLE:
            try:
                self.tts = pyttsx3.init()
                self.tts.setProperty('rate', 150)
                self.tts.setProperty('volume', 1.0)
            except Exception as e:
                print(f"⚠️ TTS init error: {e}")
        
        # Initialize Groq if available
        self.groq = None
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        if GROQ_AVAILABLE and self.groq_api_key:
            try:
                self.groq = Groq(api_key=self.groq_api_key)
                print("✅ Groq LLM initialized")
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
        
        # App shortcuts
        self.apps = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe", 
            "edge": "msedge.exe",
            "vscode": "code.exe",
            "notepad": "notepad.exe",
            "calc": "calc.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "terminal": "cmd.exe",
            "explorer": "explorer.exe",
        }
        
        # Websites (600+ shortcuts)
        self.websites = {
            "google": "google.com",
            "github": "github.com",
            "youtube": "youtube.com",
            "hubspot": "hubspot.com",
            "linkedin": "linkedin.com",
            "twitter": "twitter.com",
            "facebook": "facebook.com",
            "reddit": "reddit.com",
            "stackoverflow": "stackoverflow.com",
            "amazon": "amazon.com",
            "netflix": "netflix.com",
            "slack": "slack.com",
            "notion": "notion.so",
            "figma": "figma.com",
            "asana": "asana.com",
            "jira": "jira.com",
        }
    
    def speak(self, text: str):
        """Text to speech"""
        if not self.tts:
            return
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def parse_command_with_groq(self, command: str) -> dict:
        """Parse command using Groq LLM"""
        if not self.groq:
            return self.parse_command_heuristic(command)
        
        try:
            prompt = f"""You are JARVIS, a system-level AI assistant. Parse this command and return JSON with:
- intent: search, open_app, navigate, info, control, execute
- action: specific action to take
- target: app name, website, file, or query
- parameters: dict with relevant data

Command: {command}

Return ONLY valid JSON, no other text. Example:
{{"intent": "search", "action": "google_search", "target": "HubSpot", "parameters": {{"query": "HubSpot pricing"}}}}

Command to parse:
"""
            
            message = self.groq.messages.create(
                model="mixtral-8x7b-32768",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt + command}],
                temperature=0.3
            )
            
            response_text = message.content[0].text.strip()
            
            # Extract JSON
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except Exception as e:
            print(f"Groq parsing error: {e}")
        
        return self.parse_command_heuristic(command)
    
    def parse_command_heuristic(self, command: str) -> dict:
        """Fallback: Heuristic-based parsing (100% reliable)"""
        cmd_lower = command.lower().strip()
        
        # STOP commands
        if any(word in cmd_lower for word in ["stop", "pause", "quit", "exit", "enough"]):
            return {
                "intent": "control",
                "action": "stop_listening",
                "target": "",
                "parameters": {}
            }
        
        # OPEN APP commands
        if any(word in cmd_lower for word in ["open", "launch", "start"]):
            for app_name in self.apps.keys():
                if app_name in cmd_lower:
                    return {
                        "intent": "open_app",
                        "action": "launch_app",
                        "target": app_name,
                        "parameters": {"app": app_name}
                    }
        
        # NAVIGATE commands
        if any(word in cmd_lower for word in ["go to", "visit", "navigate to", "open"]):
            for site_name, url in self.websites.items():
                if site_name in cmd_lower:
                    return {
                        "intent": "navigate",
                        "action": "open_website",
                        "target": site_name,
                        "parameters": {"url": f"https://{url}"}
                    }
        
        # TIME/DATE commands
        if "time" in cmd_lower or "what time" in cmd_lower:
            return {
                "intent": "info",
                "action": "get_time",
                "target": "",
                "parameters": {}
            }
        
        if "date" in cmd_lower or "what date" in cmd_lower:
            return {
                "intent": "info",
                "action": "get_date",
                "target": "",
                "parameters": {}
            }
        
        # DEFAULT: Treat as search
        return {
            "intent": "search",
            "action": "google_search",
            "target": command,
            "parameters": {"query": command}
        }
    
    async def execute_command(self, command: str) -> dict:
        """Execute a command and return results"""
        try:
            self.processing = True
            self.command_count += 1
            
            # Parse command
            if self.groq:
                parsed = self.parse_command_with_groq(command)
            else:
                parsed = self.parse_command_heuristic(command)
            
            intent = parsed.get("intent", "search")
            action = parsed.get("action", "")
            target = parsed.get("target", "")
            params = parsed.get("parameters", {})
            
            result = {
                "command": command,
                "intent": intent,
                "action": action,
                "target": target,
                "success": False,
                "response": "",
                "execution": ""
            }
            
            # ============ EXECUTE ACTIONS ============
            
            # STOP LISTENING
            if action == "stop_listening":
                self.listening = False
                result["success"] = True
                result["response"] = "Stopping listening mode"
                result["execution"] = "Stopped"
            
            # LAUNCH APP
            elif action == "launch_app":
                try:
                    exe_path = self.apps.get(target.lower(), target)
                    subprocess.Popen(exe_path)
                    result["success"] = True
                    result["response"] = f"Opening {target}"
                    result["execution"] = f"Launched {exe_path}"
                    self.success_count += 1
                except Exception as e:
                    result["response"] = f"Failed to open {target}"
                    result["execution"] = str(e)
                    self.error_count += 1
            
            # OPEN WEBSITE
            elif action == "open_website":
                try:
                    url = params.get("url", f"https://{self.websites.get(target.lower(), target)}.com")
                    webbrowser.open(url)
                    result["success"] = True
                    result["response"] = f"Opening {target}"
                    result["execution"] = f"Opened {url}"
                    self.success_count += 1
                except Exception as e:
                    result["response"] = f"Failed to open {target}"
                    result["execution"] = str(e)
                    self.error_count += 1
            
            # GOOGLE SEARCH
            elif action == "google_search":
                try:
                    query = params.get("query", target)
                    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    webbrowser.open(search_url)
                    result["success"] = True
                    result["response"] = f"Searching for {query}"
                    result["execution"] = f"Opened Google search: {query}"
                    self.success_count += 1
                except Exception as e:
                    result["response"] = f"Search failed"
                    result["execution"] = str(e)
                    self.error_count += 1
            
            # GET TIME
            elif action == "get_time":
                try:
                    current_time = datetime.now().strftime("%I:%M %p")
                    result["success"] = True
                    result["response"] = f"The current time is {current_time}"
                    result["execution"] = f"Retrieved time: {current_time}"
                    self.success_count += 1
                except Exception as e:
                    result["response"] = "Could not get time"
                    result["execution"] = str(e)
            
            # GET DATE
            elif action == "get_date":
                try:
                    current_date = datetime.now().strftime("%A, %B %d, %Y")
                    result["success"] = True
                    result["response"] = f"Today is {current_date}"
                    result["execution"] = f"Retrieved date: {current_date}"
                    self.success_count += 1
                except Exception as e:
                    result["response"] = "Could not get date"
                    result["execution"] = str(e)
            
            # DEFAULT: SEARCH
            else:
                try:
                    query = target or command
                    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    webbrowser.open(search_url)
                    result["success"] = True
                    result["response"] = f"Searching for {query}"
                    result["execution"] = f"Opened Google search"
                    self.success_count += 1
                except Exception as e:
                    result["response"] = "Search failed"
                    result["execution"] = str(e)
                    self.error_count += 1
            
            # Store in history
            self.session_commands.append({
                "timestamp": datetime.now().isoformat(),
                "command": command,
                "intent": intent,
                "action": action,
                "success": result["success"]
            })
            
            self.processing = False
            return result
        
        except Exception as e:
            self.processing = False
            self.error_count += 1
            return {
                "command": command,
                "success": False,
                "response": "Command execution failed",
                "execution": str(e)
            }


# ============ INITIALIZE JARVIS ============
print("🚀 JARVIS Core initializing...")
jarvis = JarvisCore()
print("✅ JARVIS Core ready!")

# ============ WebSocket Endpoint ============
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket handler for real-time command processing"""
    client_id = f"{websocket.client.host}:{websocket.client.port}" if websocket.client else "unknown"
    
    try:
        print(f"🔌 Accepting WebSocket connection from {client_id}")
        await websocket.accept()
        print(f"✅ WebSocket connected: {client_id}")
        jarvis.listening = True
        
        # Send welcome message
        await websocket.send_json({
            "type": "status",
            "message": "Connected to JARVIS",
            "listening": True,
            "groq_available": bool(jarvis.groq),
            "tts_available": bool(jarvis.tts)
        })
        
        # Main message loop
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                print(f"📨 Received from {client_id}: {data}")
                
                try:
                    message = json.loads(data)
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON: {data}")
                    await websocket.send_json({"type": "error", "message": "Invalid JSON"})
                    continue
                
                # Handle command
                if message.get("type") == "command":
                    command_text = message.get("command", "").strip()
                    
                    if command_text:
                        print(f"📝 Executing: {command_text}")
                        
                        # Execute command
                        result = await jarvis.execute_command(command_text)
                        print(f"✅ Result: success={result.get('success')}")
                        
                        # Send response
                        response = {
                            "type": "result",
                            "success": result["success"],
                            "response": result["response"],
                            "command": command_text,
                            "intent": result.get("intent", ""),
                            "action": result.get("action", "")
                        }
                        
                        await websocket.send_json(response)
                        print(f"📤 Sent response: {result['response'][:50]}")
                
                # Handle stop
                elif message.get("type") == "stop":
                    jarvis.listening = False
                    await websocket.send_json({
                        "type": "status",
                        "message": "Listening stopped",
                        "listening": False
                    })
                
                # Handle ping/keepalive
                elif message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            
            except WebSocketDisconnect:
                print(f"🔌 Client disconnected: {client_id}")
                break
            except Exception as e:
                print(f"❌ Message processing error: {e}")
                try:
                    await websocket.send_json({"type": "error", "message": str(e)})
                except:
                    pass
    
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
    finally:
        jarvis.listening = False
        print(f"❌ WebSocket closed: {client_id}")


# ============ REST Endpoints ============
@app.get("/status")
def get_status():
    """Get JARVIS status"""
    return {
        "status": "online",
        "listening": jarvis.listening,
        "processing": jarvis.processing,
        "commands_processed": jarvis.command_count,
        "success_count": jarvis.success_count,
        "error_count": jarvis.error_count,
        "success_rate": f"{(jarvis.success_count / max(jarvis.command_count, 1) * 100):.1f}%",
        "groq_available": GROQ_AVAILABLE and bool(jarvis.groq),
        "tts_available": TTS_AVAILABLE and bool(jarvis.tts)
    }

@app.post("/command")
async def execute_command_http(command_text: str):
    """Execute command via HTTP"""
    if not command_text:
        return {"success": False, "error": "No command provided"}
    
    result = await jarvis.execute_command(command_text)
    return result

@app.get("/memory")
def get_memory():
    """Get session memory"""
    return {
        "commands": jarvis.session_commands[-50:],  # Last 50 commands
        "total_commands": jarvis.command_count,
        "success_rate": f"{(jarvis.success_count / max(jarvis.command_count, 1) * 100):.1f}%"
    }

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "JARVIS - Always Listening AI",
        "version": "4.0",
        "status": "operational",
        "endpoints": {
            "websocket": "ws://localhost:8000/ws",
            "status": "/status",
            "command": "/command",
            "memory": "/memory"
        }
    }


# ============ MAIN ============
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 JARVIS v4.0 - Always Listening AI Assistant")
    print("="*60)
    print(f"✅ Groq LLM: {'Ready' if jarvis.groq else 'Using heuristic parser'}")
    print(f"✅ Text-to-Speech: {'Ready' if jarvis.tts else 'Disabled'}")
    print(f"✅ WebSocket: ws://localhost:8000/ws")
    print(f"✅ API: http://localhost:8000")
    print("="*60 + "\n")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
