"""
Cross-Device Integration - Control JARVIS from mobile + laptop
Supports: Telegram Bot, API Server, WebSocket
"""

try:
    import telebot
    HAS_TELEBOT = True
except ImportError:
    HAS_TELEBOT = False

try:
    from fastapi import FastAPI
    from uvicorn import run
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


# ========== TELEGRAM BOT INTEGRATION ==========

class TelegramBotInterface:
    """Control JARVIS from Telegram on mobile"""
    
    def __init__(self, token):
        """Initialize Telegram bot"""
        if not HAS_TELEBOT:
            raise ImportError("telebot not installed: pip install pyTelegramBotAPI")
        
        self.bot = telebot.TeleBot(token)
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup message handlers"""
        
        @self.bot.message_handler(func=lambda msg: True)
        def handle_message(msg):
            """Handle any incoming message"""
            command = msg.text
            
            try:
                # Import here to avoid circular imports
                from tools.tasks import execute
                
                response = execute(command)
                self.bot.reply_to(msg, response or "Command executed")
            
            except Exception as e:
                self.bot.reply_to(msg, f"Error: {str(e)}")
    
    def start_polling(self):
        """Start bot polling (blocking)"""
        print("🤖 Telegram bot started. Send commands via Telegram!")
        self.bot.polling(none_stops=True)


def telegram_bot_server(token):
    """Run Telegram bot in background"""
    try:
        bot = TelegramBotInterface(token)
        bot.start_polling()
    except Exception as e:
        print(f"[ERROR] Telegram bot failed: {e}")


# ========== REST API INTEGRATION ==========

class JarvisAPIServer:
    """REST API for cross-device control"""
    
    def __init__(self, host="0.0.0.0", port=5000):
        if not HAS_FASTAPI:
            raise ImportError("fastapi not installed: pip install fastapi uvicorn")
        
        self.app = FastAPI(title="JARVIS API")
        self.host = host
        self.port = port
        
        self.setup_routes()
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        def root():
            return {
                "name": "JARVIS AI Assistant",
                "version": "4.0",
                "status": "online"
            }
        
        @self.app.post("/command")
        def execute_command(command: str):
            """Execute a command"""
            try:
                from tools.tasks import execute
                from brain.agent import think
                
                # Let AI think about the command
                reasoning = think(command)
                result = execute(command)
                
                return {
                    "command": command,
                    "reasoning": reasoning,
                    "result": result,
                    "status": "success"
                }
            except Exception as e:
                return {
                    "command": command,
                    "error": str(e),
                    "status": "error"
                }
        
        @self.app.get("/status")
        def get_status():
            """Get system status"""
            return {
                "name": "JARVIS",
                "status": "online",
                "mode": "API Server",
                "api_version": "1.0"
            }
        
        @self.app.post("/voice")
        def execute_voice_command(command: str):
            """Execute command with voice response"""
            try:
                from tools.tasks import execute
                from voice.speak import speak
                
                response = execute(command)
                
                # Speak response on server machine
                if response:
                    speak(response)
                
                return {
                    "command": command,
                    "response": response,
                    "status": "success"
                }
            except Exception as e:
                return {
                    "error": str(e),
                    "status": "error"
                }
    
    def start(self):
        """Start API server"""
        print(f"🚀 JARVIS API Server starting on {self.host}:{self.port}")
        print(f"📍 Base URL: http://{self.host}:{self.port}")
        print(f"📍 Docs: http://{self.host}:{self.port}/docs")
        
        run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )


# ========== WEBSOCKET INTEGRATION (Advanced) ==========

class VoiceStreamServer:
    """WebSocket server for real-time voice streaming"""
    
    def __init__(self, host="0.0.0.0", port=8000):
        """Initialize WebSocket server"""
        try:
            from fastapi import WebSocket, WebSocketDisconnect
            from fastapi.websockets import WebSocketState
            HAS_WEBSOCKET = True
        except ImportError:
            print("[WARNING] WebSocket support requires: pip install fastapi websockets")
            HAS_WEBSOCKET = False
        
        self.host = host
        self.port = port
    
    def start(self):
        """Start WebSocket server"""
        print(f"🔊 Voice Stream Server on {self.host}:{self.port}/ws")


# ========== INTEGRATION MANAGER ==========

def setup_cross_device(mode="api", **kwargs):
    """
    Setup cross-device integration
    
    Modes:
    - "telegram": Telegram bot (requires token)
    - "api": REST API server
    - "websocket": Real-time voice streaming
    """
    
    if mode == "telegram":
        token = kwargs.get("token")
        if not token:
            raise ValueError("Telegram token required")
        
        print("[SETUP] Starting Telegram bot interface...")
        return telegram_bot_server(token)
    
    elif mode == "api":
        host = kwargs.get("host", "0.0.0.0")
        port = kwargs.get("port", 5000)
        
        print("[SETUP] Starting REST API server...")
        server = JarvisAPIServer(host=host, port=port)
        server.start()
    
    elif mode == "websocket":
        print("[SETUP] Starting WebSocket server...")
        server = VoiceStreamServer()
        server.start()
    
    else:
        raise ValueError(f"Unknown mode: {mode}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "telegram":
            token = sys.argv[2] if len(sys.argv) > 2 else None
            if not token:
                print("Usage: python cross_device.py telegram YOUR_BOT_TOKEN")
                sys.exit(1)
            telegram_bot_server(token)
        
        elif mode == "api":
            setup_cross_device(mode="api")
        
        else:
            print("Usage: python cross_device.py [telegram|api|websocket]")
    else:
        print("Cross-device integration modes:")
        print("  python cross_device.py telegram YOUR_BOT_TOKEN")
        print("  python cross_device.py api")
        print("  python cross_device.py websocket")
