# Browser Module - Web search and browsing automation

import webbrowser
from config import DEBUG_MODE

def search_google(query):
    """Search query on Google"""
    try:
        if DEBUG_MODE:
            print(f"🔍 Searching Google for: {query}")
        
        # Clean up the query
        query = query.replace("search", "").strip()
        
        # Format URL
        url = f"https://www.google.com/search?q={query}"
        
        # Open in default browser
        webbrowser.open(url)
        
        return f"Searching Google for {query}"
    except Exception as e:
        return f"Error searching Google: {e}"

def search_wikipedia(query):
    """Search on Wikipedia"""
    try:
        if DEBUG_MODE:
            print(f"📚 Searching Wikipedia for: {query}")
        
        query = query.replace("wikipedia", "").strip()
        url = f"https://www.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
        
        webbrowser.open(f"https://wikipedia.org/wiki/{query.replace(' ', '_')}")
        
        return f"Searching Wikipedia for {query}"
    except Exception as e:
        return f"Error searching Wikipedia: {e}"

def open_youtube(search_query):
    """Open YouTube and search for content"""
    try:
        if DEBUG_MODE:
            print(f"📺 Opening YouTube for: {search_query}")
        
        search_query = search_query.replace("youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={search_query}"
        
        webbrowser.open(url)
        
        return f"Opening YouTube search for {search_query}"
    except Exception as e:
        return f"Error opening YouTube: {e}"

def open_github():
    """Open GitHub"""
    try:
        if DEBUG_MODE:
            print("👨‍💻 Opening GitHub...")
        
        webbrowser.open("https://www.github.com")
        
        return "Opening GitHub"
    except Exception as e:
        return f"Error opening GitHub: {e}"

def open_stack_overflow():
    """Open Stack Overflow"""
    try:
        if DEBUG_MODE:
            print("💻 Opening Stack Overflow...")
        
        webbrowser.open("https://www.stackoverflow.com")
        
        return "Opening Stack Overflow"
    except Exception as e:
        return f"Error opening Stack Overflow: {e}"

def open_chatgpt():
    """Open ChatGPT"""
    try:
        if DEBUG_MODE:
            print("🤖 Opening ChatGPT...")
        
        webbrowser.open("https://www.chatgpt.com")
        
        return "Opening ChatGPT"
    except Exception as e:
        return f"Error opening ChatGPT: {e}"

def open_copilot():
    """Open Microsoft Copilot"""
    try:
        if DEBUG_MODE:
            print("✨ Opening Microsoft Copilot...")
        
        webbrowser.open("https://copilot.microsoft.com")
        
        return "Opening Microsoft Copilot"
    except Exception as e:
        return f"Error opening Copilot: {e}"

def open_stackoverflow_ai():
    """Open Stack Overflow with AI assistance"""
    try:
        if DEBUG_MODE:
            print("💻 Opening Stack Overflow...")
        
        webbrowser.open("https://www.stackoverflow.com")
        
        return "Opening Stack Overflow for coding help"
    except Exception as e:
        return f"Error opening Stack Overflow: {e}"
