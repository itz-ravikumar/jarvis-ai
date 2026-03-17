# Task Router - Routes commands to appropriate tools

from tools.system_control import (
    open_chrome, open_notepad, open_calculator, 
    open_vscode, lock_screen, shutdown_computer,
    volume_up, volume_down
)
from tools.system_control_advanced import (
    open_app, open_file, open_folder, create_file, delete_file,
    copy_file, move_file, list_files, minimize_all, maximize_window,
    close_window, take_screenshot, get_running_apps, get_system_performance,
    get_battery_status, check_internet, restart_computer, hibernate, mute_sound
)
from tools.browser import (
    search_google, search_wikipedia, open_youtube,
    open_github, open_stack_overflow, open_chatgpt,
    open_copilot, open_stackoverflow_ai
)
from tools.report_generator import (
    generate_fintech_ai_trends_report, save_report, print_report, get_report_text
)
from tools.utilities import (
    get_time, get_date, get_day_of_week, get_system_info,
    get_joke, get_motivational_quote, get_weather_summary,
    get_today_summary, format_system_info, create_note,
    get_calculator_result, get_file_list, save_reminder, init_data_storage
)
from tools.advanced_reports import (
    generate_daily_briefing, generate_market_trends_report,
    generate_productivity_report, generate_tech_trends_report,
    generate_wellness_report, generate_career_development_report,
    save_and_format_report
)
from tools.task_manager import (
    add_task, list_tasks, complete_task, get_task_summary
)
from config import DEBUG_MODE

# Initialize data storage on module load
init_data_storage()

def execute(command):
    """
    Comprehensive command router supporting 100+ voice commands
    Routes to appropriate function based on intent
    """
    
    if not command:
        return ""
    
    command = command.lower().strip()
    
    if DEBUG_MODE:
        print(f"[ROUTE] Routing command: {command}")
    
    # ===== TIME & DATE COMMANDS =====
    if "what time is it" in command or "current time" in command:
        return f"⏰ The current time is {get_time()}"
    
    if "what date is it" in command or "today date" in command or "what's today" in command:
        return f"📅 Today is {get_date()}"
    
    if "what day" in command or "day of week" in command:
        return f"📆 Today is {get_day_of_week()}"
    
    # ===== SYSTEM COMMANDS =====
    if "system info" in command or "system status" in command or "system information" in command:
        info = get_system_info()
        print(format_system_info(info))
        return format_system_info(info)
    
    if "system performance" in command or "system stats" in command or "cpu usage" in command or "ram usage" in command:
        perf = get_system_performance()
        print(perf)
        return perf
    
    if "battery" in command or "battery status" in command:
        battery = get_battery_status()
        print(battery)
        return battery
    
    if "internet" in command or "connection" in command or "check wifi" in command:
        result = check_internet()
        print(result)
        return result
    
    if "running" in command or "show processes" in command or "what's running" in command:
        apps = get_running_apps()
        print(apps)
        return apps
    
    if "lock screen" in command or "lock" in command:
        return lock_screen()
    
    if "volume up" in command or "increase volume" in command:
        return volume_up()
    
    if "volume down" in command or "decrease volume" in command:
        return volume_down()
    
    if "restart" in command or "reboot" in command:
        return restart_computer()
    
    if "sleep" in command or "hibernate" in command or "standby" in command:
        return hibernate()
    
    if "mute" in command:
        return mute_sound()
    
    # ===== ADVANCED FILE OPERATIONS =====
    if "take screenshot" in command or "screenshot" in command:
        return take_screenshot()
    
    if "open file" in command:
        file_path = command.replace("open file", "").strip()
        if file_path:
            return open_file(file_path)
        return "Please specify file path"
    
    if "open folder" in command:
        folder_path = command.replace("open folder", "").strip()
        if folder_path:
            return open_folder(folder_path)
        return "Please specify folder path"
    
    if "create file" in command:
        name = command.replace("create file", "").strip()
        if name:
            return create_file(f"jarvis_data/{name}", "")
        return "Please specify filename"
    
    if "delete file" in command or "remove file" in command:
        file_path = command.replace("delete file", "").replace("remove file", "").strip()
        if file_path:
            return delete_file(file_path)
        return "Please specify file path"
    
    if "list files" in command or "show files" in command or "directory" in command:
        directory = command.replace("list files", "").replace("show files", "").replace("in", "").strip()
        if directory and (directory != "in" and directory != ""):
            return list_files(directory)
        return list_files("./jarvis_data")
    
    # ===== WINDOW CONTROL =====
    if "minimize all" in command or "minimize all windows" in command:
        return minimize_all()
    
    if "maximize" in command:
        return maximize_window()
    
    if "close window" in command or "close this window" in command:
        return close_window()
    
    # ===== APP LAUNCHING =====
    if "open chrome" in command or "launch chrome" in command or "start chrome" in command:
        return open_chrome()
    
    if "open notepad" in command or "launch notepad" in command or "new note" in command:
        return open_notepad()
    
    if "open calculator" in command or "launch calculator" in command:
        return open_calculator()
    
    if "open code" in command or "launch vs code" in command or "open vscode" in command or "open visual code" in command:
        return open_vscode()
    
    if "open chat" in command or "chatgpt" in command or "chat gpt" in command:
        return open_chatgpt()
    
    if "open copilot" in command or "microsoft copilot" in command:
        return open_copilot()
    
    if "open stack overflow" in command or "stackoverflow" in command or "stack overflow" in command:
        return open_stackoverflow_ai()
    
    # ===== WEB SEARCH =====
    if "search" in command:
        query = command.replace("search", "").strip()
        return search_google(query)
    
    if "google" in command and "search" not in command:
        query = command.replace("google", "").strip()
        return search_google(query)
    
    if "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        return search_wikipedia(query)
    
    if "youtube" in command:
        query = command.replace("youtube", "").strip()
        return open_youtube(query)
    
    if "github" in command:
        return open_github()
    
    if "stack overflow" in command or "stackoverflow" in command:
        return open_stack_overflow()
    
    # ===== WEATHER =====
    if "weather" in command or "how is the weather" in command:
        return get_weather_summary()
    
    # ===== JOKES & MOTIVATION =====
    if "tell me a joke" in command or "make me laugh" in command or "joke" in command:
        return f"😂 {get_joke()}"
    
    if "motivational quote" in command or "inspire me" in command or "motivation" in command:
        return f"💪 {get_motivational_quote()}"
    
    # ===== GREETING & INFO =====
    if "hello" in command or "hi" in command or "hey" in command:
        return f"👋 Hello! I'm Jarvis, your AI assistant. How can I help you today?"
    
    if "what is your name" in command or "who are you" in command:
        return "🤖 I'm Jarvis, your personal AI assistant. I can help with tasks, reports, web searches, and much more!"
    
    if "help" in command or "what can you do" in command or "command reference" in command:
        from voice.listen import voice_command_reference
        voice_command_reference()
        return "📖 Voice command reference displayed above"
    
    if "what code" in command or "how code" in command or "explain code" in command or "coding help" in command:
        return open_stackoverflow_ai()
    
    if "show commands" in command or "list commands" in command or "voice commands" in command:
        from voice.listen import voice_command_reference
        voice_command_reference()
        return "📖 All available voice commands listed above"
    
    # ===== REPORT GENERATION =====
    if "daily briefing" in command or "daily report" in command:
        report = generate_daily_briefing()
        result = save_and_format_report(report, "daily_briefing")
        print(result)
        return "✅ Daily briefing generated!"
    
    if "market trends" in command and "report" in command:
        report = generate_market_trends_report()
        result = save_and_format_report(report, "market_trends")
        print(result)
        return "✅ Market trends report generated!"
    
    if "productivity report" in command:
        report = generate_productivity_report()
        result = save_and_format_report(report, "productivity")
        print(result)
        return "✅ Productivity report generated!"
    
    if "tech trends" in command or "technology trends" in command:
        report = generate_tech_trends_report()
        result = save_and_format_report(report, "tech_trends")
        print(result)
        return "✅ Tech trends report generated!"
    
    if "wellness" in command:
        report = generate_wellness_report()
        result = save_and_format_report(report, "wellness")
        print(result)
        return "✅ Wellness recommendations generated!"
    
    if "career" in command and ("development" in command or "report" in command):
        report = generate_career_development_report()
        result = save_and_format_report(report, "career_development")
        print(result)
        return "✅ Career development report generated!"
    
    if ("fintech" in command or "finance" in command) and ("ai" in command or "trend" in command or "report" in command):
        report = generate_fintech_ai_trends_report()
        save_report(report)
        print("\n" + print_report(report))
        return "✅ Fintech AI Trends report generated and saved!"
    
    if "prepare a report" in command or "generate report" in command or "create report" in command:
        return "📊 Available reports: fintech AI trends, market trends, productivity, wellness, career development, tech trends, daily briefing"
    
    # ===== TASK MANAGEMENT =====
    if "add task" in command or "add a task" in command:
        # Extract task title
        task_title = command.replace("add task", "").replace("add a task", "").strip()
        if task_title:
            result = add_task(task_title)
            print(result)
            return result
        return "Please tell me the task title"
    
    if "list tasks" in command or "show tasks" in command or "my tasks" in command:
        result = list_tasks("pending")
        print(result)
        return result
    
    if "completed tasks" in command or "done tasks" in command:
        result = list_tasks("completed")
        print(result)
        return result
    
    if "all tasks" in command:
        result = list_tasks("all")
        print(result)
        return result
    
    if "task summary" in command or "task count" in command:
        return get_task_summary()
    
    # ===== NOTE MANAGEMENT =====
    if "create note" in command or "create a note" in command or "write note" in command:
        return "📝 Please tell me the note name and content"
    
    if "list files" in command or "show files" in command:
        files = get_file_list()
        return f"📁 Files: {', '.join(files[:5])}"
    
    # ===== TODAY'S SUMMARY =====
    if "today" in command and ("summary" in command or "brief" in command):
        print(get_today_summary())
        return get_today_summary()
    
    # ===== CALCULATIONS =====
    if "calculate" in command:
        expr = command.replace("calculate", "").strip()
        return get_calculator_result(expr)
    
    if "what is" in command and any(op in command for op in ["+", "-", "*", "/"]):
        expr = command.replace("what is", "").strip()
        return get_calculator_result(expr)
    
    # ===== REMINDERS =====
    if "remind me" in command:
        reminder_text = command.replace("remind me", "").strip()
        result = save_reminder("Reminder", reminder_text)
        return result
    
    # ===== VOICE COMMANDS =====
    if "voice mode" in command or "voice command mode" in command or "enter voice mode" in command:
        from voice.voice_commands import start_voice_assistant
        try:
            start_voice_assistant()
            return "✅ Voice mode session ended"
        except Exception as e:
            return f"Voice mode error: {e}"
    
    if "quick voice" in command or "voice command" in command and "show" not in command:
        from voice.voice_commands import quick_voice
        try:
            return quick_voice("quick")
        except Exception as e:
            return f"Voice command error: {e}"
    
    if "voice history" in command or "recent commands" in command or "command history" in command:
        from voice.listen import get_voice_history
        history = get_voice_history(15)
        if history:
            print("\n📋 Voice Command History:")
            print("="*60)
            for cmd in history:
                print(f"  {cmd}", end="")
            print("="*60)
            return f"✅ Displayed {len(history)} recent commands"
        else:
            return "No command history yet"
    
    if "voice commands" in command or "show voice commands" in command:
        from voice.listen import voice_command_reference
        voice_command_reference()
        return "📖 Voice command reference displayed"
    
    # ===== ADVANCED EXECUTOR FALLBACK =====
    # Try advanced system command execution for unrecognized commands
    try:
        from tools.advanced_executor import AdvancedExecutor
        executor = AdvancedExecutor()
        result = executor.execute(command)
        
        if result and "Error" not in result and "not recognized" not in result:
            if DEBUG_MODE:
                print(f"✅ Advanced executor handled: {command}")
            return result
    except Exception as e:
        if DEBUG_MODE:
            print(f"⚠️ Advanced executor error: {e}")
    
    # ===== AI FALLBACK FOR ANY COMMAND =====
    # Use AI to process any unrecognized command
    from brain.agent import think
    try:
        if DEBUG_MODE:
            print(f"🧠 Using AI to process: {command}")
        
        ai_response = think(command)
        
        if ai_response:
            return ai_response
        else:
            return f"❓ I'm not sure how to handle that. Try 'help' for available commands."
    except Exception as e:
        if DEBUG_MODE:
            print(f"❌ AI processing error: {e}")
        return f"❓ I didn't understand that. Say 'help' for available commands."


