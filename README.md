# 🤖 JARVIS - Voice-Controlled AI Assistant (v4.0)

> **Production-Ready Voice AI with Free LLM Support**  
> **Status**: ✅ Fully Implemented | **Uses**: Python 3.14 | **OS**: Windows

---

## 📖 TABLE OF CONTENTS

1. [Quick Start (5 Minutes)](#-quick-start-5-minutes)
2. [Project Overview](#-project-overview)
3. [Installation & Setup](#️-installation--setup)
4. [Free AI Options](#-free-ai-options)
5. [Voice Commands Reference](#-voice-commands-reference)
6. [System Control Features](#-system-control-features)
7. [Advanced Features](#-advanced-features)
8. [Troubleshooting](#-troubleshooting)

---

## ⚡ Quick Start (5 Minutes)

### Option 1: No AI Mode (Zero Setup)
```bash
cd c:\Users\hp\Desktop\New folder (2)\jarvis_ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
# Choose: 1 (text commands) → Type: "search python"
```

### Option 2: With Free Groq API (Recommended)
```bash
# 1. Get free API key: https://console.groq.com (2 min)
# 2. Add to config.py: USE_GROQ = True & GROQ_API_KEY = "your_key"
# 3. Run:
python main.py
# Choose: 2 (voice mode) → Speak: "search artificial intelligence"
```

### Option 3: With Ollama (Offline AI)
```bash
# 1. Download: https://ollama.ai
# 2. Run: ollama serve (in separate terminal)
# 3. Download model: ollama pull mistral
# 4. Edit config.py: USE_OLLAMA = True
# 5. Run: python main.py
```

---

## 🎯 Project Overview

### What is JARVIS?
JARVIS is a **voice-controlled AI assistant** that:
- ✅ Listens to voice commands
- ✅ Processes with AI reasoning (Groq, Ollama, or local)
- ✅ Executes 100+ system commands
- ✅ Remembers user preferences
- ✅ Works with wake word detection ("Hey Jarvis")
- ✅ Runs as background service

### Architecture
```
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  VOICE IN   │────▶│  AI BRAIN│────▶│  TOOLS   │────▶│ VOICE OUT│
│             │     │          │     │          │     │          │
│• Microphone │     │• Groq    │     │• Web       │     │• Speaker │
│• Speech→Text│     │• Ollama  │     │• Apps      │     │• Text→Voice
└─────────────┘     └──────────┘     └──────────┘     └──────────┘
  listen.py        agent.py      system_control.py   speak.py
```

### Project Structure
```
jarvis_ai/
├── main.py                    # ⭐ START HERE
├── config.py                  # AI & voice settings
├── requirements.txt           # Dependencies
│
├── voice/                     # Voice I/O Module
│   ├── listen.py             # Speech→Text
│   ├── speak.py              # Text→Speech
│   ├── conversation.py        # Interactive mode
│   └── voice_commands.py     # Command routing
│
├── brain/                     # AI Brain Module
│   ├── agent.py              # LLM reasoning
│   ├── memory.py             # Persistent memory
│   └── smart_agent.py        # Multi-step tasks
│
├── tools/                     # System Tools
│   ├── system_control.py     # App/OS control
│   ├── browser.py            # Web search
│   ├── task_manager.py       # Task execution
│   └── report_generator.py   # Report creation
│
├── wake_word.py              # "Hey Jarvis" detection
├── service_runner.py         # Background service
└── jarvis_data/              # Data storage
    ├── memory/               # ChromaDB storage
    └── voice_commands.txt    # Command history
```

---

## 🖥️ Installation & Setup

### Phase 1: Environment Setup (5 minutes)

**Step 1: Navigate to project**
```bash
cd "c:\Users\hp\Desktop\New folder (2)\jarvis_ai"
```

**Step 2: Create virtual environment**
```bash
python -m venv venv
```

**Step 3: Activate it**
```bash
venv\Scripts\activate
```

**Step 4: Upgrade pip**
```bash
python -m pip install --upgrade pip
```

### Phase 2: Install Dependencies

**Option A: Full Installation (All Features)**
```bash
pip install -r requirements.txt
```

**Option B: Minimal Installation (Command Mode Only)**
```bash
pip install requests pyautogui
```

### Phase 3: Run JARVIS

```bash
python main.py
```

**Main Menu:**
```
1. Text commands (type) ← Start here!
2. Voice mode (speak)
3. Quick voice (single command)
4. Conversation mode (back & forth)
5. Siri mode (always listening)
6. Wake word mode (say "Hey Jarvis")
7. Smart agent mode (multi-step tasks)
8. Show all commands
9. Settings
10. Exit
```

---

## 🆓 Free AI Options

Choose **ONE** AI option. All are completely FREE.

### 🥇 Option 1: Groq (BEST - Recommended) ⭐

**Fastest & Easiest Setup**

**Pros:**
- ✅ FREE (no credit card)
- ✅ Super fast inference
- ✅ Powerful model (Mixtral-8x7b)
- ✅ 5-minute setup
- ✅ No local GPU needed

**Setup:**
```bash
# 1. Get free API key: https://console.groq.com
# 2. Edit config.py:
USE_GROQ = True
GROQ_API_KEY = "gsk_your_key_here"

USE_OPENAI = False
USE_OLLAMA = False
USE_NO_AI = False

# 3. Run:
python main.py
```

---

### 🟢 Option 2: Ollama (Offline & Private) 🔐

**Complete Privacy - Works Offline**

**Pros:**
- ✅ 100% offline (no internet needed)
- ✅ Complete privacy
- ✅ Free & open-source
- ✅ No API key required
- ✅ Multiple models available

**Setup:**

1. **Download Ollama**: https://ollama.ai

2. **Download a model** (run once):
```bash
ollama pull mistral
```

3. **Start Ollama** (in separate terminal):
```bash
ollama serve
# Keep this running!
```

4. **Edit config.py:**
```python
USE_OLLAMA = True
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"

USE_GROQ = False
USE_OPENAI = False
USE_NO_AI = False
```

5. **Run JARVIS:**
```bash
python main.py
```

**Popular Models:**
- `mistral` - Fast & smart (7B) ⭐
- `neural-chat` - Good conversation
- `phi` - Ultra-fast (2.7B)
- `llama2` - Powerful (7B, 13B)
- `orca-mini` - Compact & capable

**Hardware:**
- 8GB RAM minimum
- 10-20GB disk for models
- GPU optional (faster if available)

---

### 🟡 Option 3: HuggingFace (Free Cloud LLM)

**Pros:**
- ✅ Free
- ✅ Multiple models
- ✅ No credit card
- ✅ Community-driven

**Setup:**
```bash
# 1. Get token: https://huggingface.co
# 2. Edit config.py:
USE_HUGGINGFACE = True
HUGGINGFACE_API_KEY = "hf_your_token"

# 3. Run: python main.py
```

---

### 🟢 Option 4: No AI Mode (Zero Setup)

**Pros:**
- ✅ Works immediately
- ✅ No API keys
- ✅ 100% free
- ✅ Offline

**Cons:**
- ❌ No reasoning ability
- ❌ Command routing only

**Setup:**
```python
# In config.py:
USE_NO_AI = True

# Run:
python main.py
```

---

## 🎤 Voice Commands Reference

### ⏰ Time & Date
```
"what time is it"          → Shows current time
"what date is it"          → Shows current date
"what day is today"        → Shows day of week
```

### 🔍 Web Search
```
"search [query]"           → Google search
"google [query]"           → Google search
"youtube [search]"         → YouTube search
"wikipedia [topic]"        → Wikipedia search
"duckduckgo [query]"       → DuckDuckGo search
```

### 💻 Applications
```
"open chrome"              → Launch Chrome
"open firefox"             → Launch Firefox
"open notepad"             → Open Notepad
"open calculator"          → Open Calculator
"open code" / "vscode"     → Open VS Code
"open powershell"          → Open PowerShell
```

### 📁 File Operations
```
"create file [name]"       → Create new file
"delete file [name]"       → Delete file
"copy file [src] to [dst]" → Copy file
"move file [src] to [dst]" → Move file
"list files in [path]"     → List directory
"open folder [path]"       → Open folder
```

### 🖥️ System Control
```
"volume up"                → Increase volume
"volume down"              → Decrease volume
"mute"                     → Mute sound
"lock screen"              → Lock Windows
"shutdown"                 → Shutdown (30s delay)
"restart"                  → Restart computer
"sleep"                    → Hibernate
"minimize all"             → Minimize all windows
"maximize window"          → Maximize current window
```

### 📊 System Info
```
"system performance"       → CPU/RAM/Disk usage
"battery"                  → Battery status
"check internet"           → Test connection
"wifi"                     → WiFi status
"running apps"             → List processes
```

### 🎯 Jarvis Control
```
"voice history"            → Show recent commands
"voice commands"           → Show all commands
"remember [info]"          → Save preference
"what do you remember"     → Recall preferences
"stop" / "exit"            → Stop JARVIS
```

---

## 🖥️ System Control Features

### 1. Application Control
```
"open notepad"             → Launch app
"close window"             → Close active window
"minimize all windows"     → Minimize everything
```

### 2. File & Folder Management
```
"create file test.txt"     → Create file
"delete file test.txt"     → Delete file
"copy file a.txt to b.txt" → Copy with new name
"list files on Desktop"    → List directory
```

### 3. Keyboard & Mouse
```
"type hello world"         → Type text
"press enter"              → Press key
"ctrl+c"                   → Hotkey
"click at 500 300"         → Click coordinates
"move mouse to 100 200"    → Move mouse
```

### 4. Screenshot
```
"take screenshot"          → Capture screen
"screenshot"               → Save to jarvis_data/
```

### 5. Audio Control
```
"volume up"                → Increase system volume
"volume down"              → Decrease system volume
"mute"                     → Mute speakers
```

### 6. Screen Management
```
"lock screen"              → Lock Windows
"shutdown"                 → Shutdown (30s countdown)
"restart"                  → Restart (60s countdown)
"sleep"                    → Sleep mode
```

---

## 🚀 Advanced Features

### 1. Wake Word Detection 🔥
**Say "Hey Jarvis" to activate**

```bash
python main.py
# Choose: 6 (wake word mode)
# Say: "Hey Jarvis, search AI news"
```

**Note:** Requires Porcupine (free 30-day access)

### 2. Smart Agent (Multi-Step Tasks) 🤖
**AI-powered workflow automation**

```bash
python main.py
# Choose: 7 (smart agent mode)
# Say: "Prepare a fintech report with latest trends"
# Agent breaks down into steps and executes
```

**Examples:**
- "Generate quarterly report with charts"
- "Create presentation on AI trends"
- "Research and summarize blockchain news"

### 3. Memory System 🧠
**JARVIS learns your preferences**

```bash
Say: "Remember that I like dark mode"
Say: "Remember to use Groq API"

# Later:
Say: "What do you remember about my preferences?"
```

### 4. Conversation Mode ⭐
**Back-and-forth dialogue**

```bash
python main.py
# Choose: 4 (conversation mode)
# Have multi-turn conversation with JARVIS
```

### 5. Background Service 🔄
**Runs even after closing terminal**

```bash
python main.py
# Choose: 9 (settings)
# Choose: 3 (install background service)
```

---

## ⚙️ Configuration

Edit `config.py` to customize JARVIS:

```python
# ===== AI SELECTION =====
USE_GROQ = True              # Use Groq (FREE)
USE_OLLAMA = False           # Use Ollama (offline)
USE_OPENAI = False           # Use OpenAI (paid)
USE_HUGGINGFACE = False      # Use HuggingFace (free)
USE_NO_AI = False            # No reasoning

# ===== API KEYS =====
GROQ_API_KEY = "your_key"
OPENAI_API_KEY = "your_key"
HUGGINGFACE_API_KEY = "your_key"

# ===== VOICE SETTINGS =====
VOICE_SPEED = 150            # Words per minute
VOICE_VOLUME = 1.0           # 0.0 to 1.0

# ===== OTHER =====
DEBUG_MODE = False           # Enable debugging
ASSISTANT_NAME = "Jarvis"    # Assistant name
```

---

## 🧪 Testing

### Test 1: Simple Installation
```bash
python test_simple.py        # Basic functionality test
```

### Test 2: Full System Demo
```bash
python test_full_demo.py     # Complete feature demo
```

### Test 3: Production System
```bash
python test_production_system.py  # Production checks
```

### Test 4: System Control
```bash
python test_system_control.py     # Control features
```

---

## 🆘 Troubleshooting

### "Microphone not found"
```bash
# Install PortAudio:
# Windows: http://www.portaudio.com/download.html
pip install pyaudio
```

### "API key error"
```bash
# 1. Check config.py has correct key
# 2. Make sure key is NOT expired
# 3. Verify internet connection
# 4. For Groq: https://console.groq.com/keys
```

### "Ollama connection refused"
```bash
# Make sure Ollama is running in separate terminal:
ollama serve
# Keep that terminal open while using JARVIS
```

### "Speech recognition not working"
```bash
# 1. Check microphone in Windows sound settings
# 2. Test volume levels
# 3. Try upgrading SpeechRecognition:
pip install --upgrade SpeechRecognition

# 4. For more debug info:
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"
```

### "Commands not executing"
```bash
# 1. Check command spelling/format
# 2. Try text mode first (type instead of voice)
# 3. Enable DEBUG_MODE in config.py
# 4. Check jarvis_data/ folder permissions
```

### "Slow responses"
```bash
# Use Groq instead of Ollama
# Groq is optimized for speed
# Or use HuggingFace (faster than Ollama)

# In config.py:
USE_GROQ = True
USE_OLLAMA = False
```

---

## 📚 File Reference

| File | Purpose |
|------|---------|
| `main.py` | **Main entry point** - Start here |
| `config.py` | Settings & API keys |
| `requirements.txt` | Python dependencies |
| `voice/listen.py` | Speech recognition |
| `voice/speak.py` | Text-to-speech |
| `voice/conversation.py` | Interactive mode |
| `brain/agent.py` | AI reasoning |
| `brain/memory.py` | Persistent memory |
| `brain/smart_agent.py` | Task automation |
| `tools/system_control.py` | App/OS control |
| `tools/browser.py` | Web search |
| `tools/task_manager.py` | Command router |
| `wake_word.py` | Wake word detection |
| `service_runner.py` | Background service |

---

## 🎓 Learning Resources

### Getting Started
- Start with Option 4 (No AI Mode) to test basic functionality
- Progress to Option 1 (Groq) for AI features
- Try Option 2 (Ollama) for offline usage

### System Control
- Test with text commands first: `python main.py` → Type commands
- Progress to voice mode with confirmation enabled
- Advanced: Use smart agent for complex tasks

### Memory & Learning
- Use "Remember" command to save preferences
- Check saved preferences with "What do you remember?"
- Memory is persistent across sessions

---

## ✅ Feature Checklist

- [x] Voice input/output (microphone & speaker)
- [x] 100+ voice commands
- [x] System control (apps, files, keyboard, mouse)
- [x] Web search (Google, YouTube, Wikipedia)
- [x] Memory system (ChromaDB)
- [x] Smart agent (multi-step tasks)
- [x] Wake word detection ("Hey Jarvis")
- [x] Free LLM support (Groq, Ollama, HuggingFace)
- [x] Background service
- [x] Multiple conversation modes
- [x] Full offline capability
- [x] Screenshot capture
- [x] System monitoring

---

## 🚀 Next Steps

1. **Quick Test**: `python main.py` → Choose option 1 → Type commands
2. **Get Free API**: https://console.groq.com (2 minutes)
3. **Enable AI**: Update config.py with your Groq key
4. **Voice Test**: Run main.py → Choose option 2 → Speak commands
5. **Memory**: Say "Remember that..." to save preferences
6. **Smart Tasks**: Use option 7 for multi-step automation
7. **Background**: Set as Windows service in option 9

---

## 📞 Support

**Issue?** Check:
1. [Troubleshooting](#-troubleshooting) section above
2. Verify all dependencies: `pip install -r requirements.txt`
3. Test installation: `python test_simple.py`
4. Enable DEBUG_MODE in config.py

**Version**: 4.0 (March 2026)  
**Status**: ✅ Production Ready  
**License**: MIT  

---

**Happy commanding!** 🎉
