# AI Agent Module - Multiple LLM backends (free and paid)

from config import (
    USE_GROQ, GROQ_API_KEY,
    USE_OPENAI, OPENAI_API_KEY,
    USE_OLLAMA, OLLAMA_URL, OLLAMA_MODEL,
    USE_HUGGINGFACE, HUGGINGFACE_API_KEY,
    USE_NO_AI, DEBUG_MODE
)
import requests

# ========== GROQ (FREE - Recommended) ==========
if USE_GROQ and GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
        if DEBUG_MODE:
            print("✅ Using Groq (Free LLM)")
    except ImportError:
        if DEBUG_MODE:
            print("⚠️  Groq library not installed: pip install groq")
        groq_client = None

# ========== OPENAI (PAID) ==========
if USE_OPENAI and OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        if DEBUG_MODE:
            print("✅ Using OpenAI")
    except ImportError:
        if DEBUG_MODE:
            print("⚠️  OpenAI library not installed: pip install openai")
        openai_client = None

# ========== OLLAMA (FREE - Local) ==========
if USE_OLLAMA:
    if DEBUG_MODE:
        print("✅ Using Ollama (Local LLM)")

# =========================================

def think(command):
    """
    Use AI to understand and reason about user command
    Supports multiple free and paid LLM backends
    """
    
    if not command:
        return None
    
    # Priority order: Groq → OpenAI → Ollama → HuggingFace
    
    # 1. Try Groq (FREE - Recommended)
    if USE_GROQ and GROQ_API_KEY and groq_client:
        try:
            if DEBUG_MODE:
                print("🧠 Groq is thinking...")
            
            message = groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Jarvis, an AI assistant. Be concise and helpful."
                    },
                    {"role": "user", "content": command}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            result = message.choices[0].message.content
            if DEBUG_MODE:
                print(f"💭 Groq: {result}")
            return result
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Groq Error: {e}")
            return None
    
    # 2. Try OpenAI (PAID)
    if USE_OPENAI and OPENAI_API_KEY and openai_client:
        try:
            if DEBUG_MODE:
                print("🧠 OpenAI is thinking...")
            
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis, an AI assistant."},
                    {"role": "user", "content": command}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            result = response.choices[0].message.content
            if DEBUG_MODE:
                print(f"💭 OpenAI: {result}")
            return result
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ OpenAI Error: {e}")
            return None
    
    # 3. Try Ollama (FREE - Local)
    if USE_OLLAMA:
        try:
            if DEBUG_MODE:
                print("🧠 Ollama is thinking...")
            
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": command,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "")
                if DEBUG_MODE:
                    print(f"💭 Ollama: {result}")
                return result
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Ollama Error: {e}")
            return None
    
    # 4. Try HuggingFace (FREE)
    if USE_HUGGINGFACE and HUGGINGFACE_API_KEY:
        try:
            if DEBUG_MODE:
                print("🧠 HuggingFace is thinking...")
            
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
                headers=headers,
                json={"inputs": command},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if DEBUG_MODE:
                    print(f"💭 HuggingFace: {result}")
                return str(result)
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ HuggingFace Error: {e}")
            return None
    
    # 5. Fallback - No AI
    if USE_NO_AI or not (GROQ_API_KEY or OPENAI_API_KEY or USE_OLLAMA or HUGGINGFACE_API_KEY):
        if DEBUG_MODE:
            print("ℹ️  No AI configured, using command routing")
        return None

def intent_detection(command):
    """
    Detect the intent behind user command
    Works with any configured LLM
    """
    
    if not command:
        return {"intent": "unknown", "confidence": 0.0}
    
    # Use same LLM backend as think()
    if USE_GROQ and GROQ_API_KEY and groq_client:
        try:
            response = groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "system",
                        "content": "Detect intent. Respond in JSON: {\"intent\": \"name\", \"confidence\": 0.0-1.0}"
                    },
                    {"role": "user", "content": command}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            import json
            result_text = response.choices[0].message.content
            
            try:
                return json.loads(result_text)
            except:
                return {"intent": "unknown", "confidence": 0.5}
        except:
            return {"intent": "unknown", "confidence": 0.0}
    
    return {"intent": "unknown", "confidence": 0.0}
