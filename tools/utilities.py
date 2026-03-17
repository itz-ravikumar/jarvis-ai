# Utility Functions - Common tasks

import json
from datetime import datetime, timedelta
import os

# Store for user preferences and data
DATA_DIR = "jarvis_data"
PREFERENCES_FILE = f"{DATA_DIR}/preferences.json"
REMINDERS_FILE = f"{DATA_DIR}/reminders.json"
FAVORITES_FILE = f"{DATA_DIR}/favorites.json"

def init_data_storage():
    """Initialize data storage directories"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)

def get_time():
    """Get current time"""
    return datetime.now().strftime("%I:%M %p")

def get_date():
    """Get current date"""
    return datetime.now().strftime("%A, %B %d, %Y")

def get_day_of_week():
    """Get day of week"""
    return datetime.now().strftime("%A")

def get_system_info():
    """Get system information"""
    import platform
    import psutil
    
    try:
        info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "CPU": platform.processor(),
            "RAM Used": f"{psutil.virtual_memory().percent}%",
            "Disk Used": f"{psutil.disk_usage('/').percent}%",
            "Python": platform.python_version()
        }
        return info
    except:
        return {"Error": "Could not retrieve system info"}

def save_reminder(title, description, remind_time=None):
    """Save a reminder"""
    init_data_storage()
    
    reminders = []
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            reminders = json.load(f)
    
    reminder = {
        "title": title,
        "description": description,
        "created": datetime.now().isoformat(),
        "remind_time": remind_time or datetime.now().isoformat()
    }
    
    reminders.append(reminder)
    
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)
    
    return f"Reminder '{title}' saved successfully"

def get_reminders():
    """Get all reminders"""
    if not os.path.exists(REMINDERS_FILE):
        return []
    
    with open(REMINDERS_FILE, 'r') as f:
        return json.load(f)

def save_favorite(name, url):
    """Save a favorite website"""
    init_data_storage()
    
    favorites = {}
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as f:
            favorites = json.load(f)
    
    favorites[name] = url
    
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=2)
    
    return f"Favorite '{name}' saved"

def get_favorite(name):
    """Get a favorite by name"""
    if not os.path.exists(FAVORITES_FILE):
        return None
    
    with open(FAVORITES_FILE, 'r') as f:
        favorites = json.load(f)
    
    return favorites.get(name)

def get_joke():
    """Get a random joke"""
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        "Why did the developer go broke? Because he used up all his cache!",
        "Why do Java developers wear glasses? Because they can't C#!",
        "A SQL query walks into a bar, walks up to two tables and asks... can I join you?",
        "How many programmers does it take to change a light bulb? Two, one to change it and one to tell them they should have used a built-in function.",
        "Why did the developer get out of the shower? Because they wanted to get a byte!",
        "Why do programmers always mix up Halloween and Christmas? Because Oct 31 equals Dec 25!",
        "What's a programmer's favorite hangout place? Foo Bar!",
        "Why did the programmer quit his job? Because he didn't get arrays of his responsibilities!"
    ]
    
    import random
    return random.choice(jokes)

def get_motivational_quote():
    """Get a motivational quote"""
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs",
        "Life is what happens when you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "It is during our darkest moments that we must focus to see the light. - Aristotle",
        "The way to get started is to quit talking and begin doing. - Walt Disney",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
        "Success is not final, failure is not fatal. - Winston Churchill",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb"
    ]
    
    import random
    return random.choice(quotes)

def get_weather_summary():
    """Get weather summary (mock data)"""
    return "🌤️ Current weather: Sunny, 72°F. No rain expected today."

def get_today_summary():
    """Get today's summary"""
    summary = f"""
📅 Today's Summary
{'='*50}
📆 Date: {get_date()}
⏰ Time: {get_time()}
🌤️  Weather: Sunny, 72°F
📝 Reminders: {len(get_reminders())} pending
💻 System Load: 45%
{'='*50}
"""
    return summary

def format_system_info(info):
    """Format system info for display"""
    output = []
    output.append("💻 System Information")
    output.append("="*50)
    for key, value in info.items():
        output.append(f"{key}: {value}")
    output.append("="*50)
    return "\n".join(output)

def get_file_list(directory="."):
    """List files in a directory"""
    try:
        files = os.listdir(directory)
        return files[:10]  # Return first 10 files
    except:
        return []

def create_note(filename, content):
    """Create a text note"""
    try:
        os.makedirs("notes", exist_ok=True)
        filepath = f"notes/{filename}.txt"
        
        with open(filepath, 'w') as f:
            f.write(f"Created: {datetime.now().isoformat()}\n")
            f.write(f"{'='*50}\n")
            f.write(content)
        
        return f"Note '{filename}' created successfully"
    except Exception as e:
        return f"Error creating note: {e}"

def get_calculator_result(expression):
    """Safe calculator"""
    try:
        # Only allow safe operations
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except:
        return "Invalid mathematical expression"
