@echo off
REM ============================================
REM Jarvis AI Assistant - Quick Install Script
REM ============================================

echo.
echo ========================================
echo   JARVIS AI ASSISTANT - QUICK SETUP
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo [4/5] Installing basic dependencies...
pip install SpeechRecognition pyttsx3 pyautogui requests --quiet

echo [5/5] Installing Groq (Free AI)...
pip install groq --quiet

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Get FREE Groq API key: https://console.groq.com
echo 2. Edit config.py and add your API key
echo 3. Run: python main.py
echo.
echo For offline AI, install Ollama instead:
echo ollama.ai
echo.
pause
