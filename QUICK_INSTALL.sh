#!/bin/bash
# Jarvis AI Assistant - Quick Install Script (Mac/Linux)

echo ""
echo "========================================"
echo "  JARVIS AI ASSISTANT - QUICK SETUP"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Upgrading pip..."
pip install --upgrade pip --quiet

echo "[4/5] Installing basic dependencies..."
pip install SpeechRecognition pyttsx3 pyautogui requests --quiet

echo "[5/5] Installing Groq (Free AI)..."
pip install groq --quiet

echo ""
echo "========================================"
echo "  SETUP COMPLETE!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Get FREE Groq API key: https://console.groq.com"
echo "2. Edit config.py and add your API key"
echo "3. Run: python main.py"
echo ""
echo "For offline AI, install Ollama instead:"
echo "ollama.ai"
echo ""
