# Configuration file for Jarvis AI
# Add your API keys and settings here

import os

# ========== AI CONFIGURATION (Choose ONE) ==========

# Option 1: Groq API (FREE - Recommended) ⭐
# Sign up: https://console.groq.com
USE_GROQ = True  # ✅ PRODUCTION: Enabled for intelligence
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "gsk_your_api_key_here")  # Add your key here

# Option 2: OpenAI API (PAID - Optional)
USE_OPENAI = False
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Option 3: Ollama (FREE - Local LLM)
# Install from: https://ollama.ai
USE_OLLAMA = False
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"

# Option 4: HuggingFace (FREE)
USE_HUGGINGFACE = False
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# Option 5: No AI (Just command routing - works offline)
USE_NO_AI = False  # ✅ PRODUCTION: Disabled - use AI instead

# ===================================================

# Voice Configuration
VOICE_SPEED = 150  # Speech speed (words per minute)
VOICE_VOLUME = 1.0  # Volume (0.0 to 1.0)

# System Configuration
DEBUG_MODE = False  # Set to False to avoid emoji issues in PowerShell  # Set to True for debugging
ASSISTANT_NAME = "Jarvis"

# Automation Configuration
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/jarvis"  # If using n8n
