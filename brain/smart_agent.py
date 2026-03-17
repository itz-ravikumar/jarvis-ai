"""
Smart Agent - Multi-step task execution
Enables advanced reasoning and automation workflows
"""

from langchain_groq import ChatGroq
import requests
import json
from config import DEBUG_MODE, USE_GROQ, GROQ_API_KEY, N8N_WEBHOOK_URL
from brain.memory import recall_memory, save_memory

try:
    from tools.report_generator import generate_fintech_report
except ImportError:
    def generate_fintech_report():
        return "Report generation not available"

try:
    from tools.system_control import execute_system_command
except ImportError:
    def execute_system_command(task):
        return f"System control not available for: {task}"

try:
    from langchain_community.tools import DuckDuckGoSearchRun
    HAS_DUCKDUCKGO = True
except ImportError:
    HAS_DUCKDUCKGO = False


# ========== SIMPLE TOOLS ==========

def search_web(query: str) -> str:
    """Search the web for information"""
    try:
        if HAS_DUCKDUCKGO:
            search = DuckDuckGoSearchRun()
            result = search.run(query)
        else:
            result = f"Search results for '{query}' (search not available)"
        
        if DEBUG_MODE:
            print(f"🔍 Web search: {query}")
        return result
    except Exception as e:
        return f"Search error: {e}"


def get_memory_context(query: str) -> str:
    """Retrieve relevant memories and past interactions"""
    try:
        memories = recall_memory(query, top_k=5)
        if memories:
            context = "Recent memories:\n"
            for mem in memories:
                context += f"- {mem.get('command')}: {mem.get('response')}\n"
            return context
        return "No relevant memories found"
    except Exception as e:
        return f"Memory error: {e}"


def execute_system_task(task: str) -> str:
    """Execute system control tasks"""
    try:
        result = execute_system_command(task)
        if DEBUG_MODE:
            print(f"⚙️  System task: {task}")
        return result
    except Exception as e:
        return f"System task error: {e}"


def generate_report_task(report_type: str = "fintech") -> str:
    """Generate reports"""
    try:
        if report_type.lower() == "fintech":
            report = generate_fintech_report()
            return f"Generated fintech report successfully"
        return "Report type not supported"
    except Exception as e:
        return f"Report generation error: {e}"


def trigger_automation(workflow_name: str) -> str:
    """Trigger n8n automation workflows"""
    try:
        payload = {"workflow": workflow_name}
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            if DEBUG_MODE:
                print(f"🚀 Automation triggered: {workflow_name}")
            return f"Triggered {workflow_name} workflow"
        else:
            return f"Automation error: {response.text}"
    except Exception as e:
        return f"Automation error: {e}"


def get_information(query: str) -> str:
    """Get general information"""
    try:
        memories = recall_memory(query, top_k=2)
        if memories:
            return f"From memory: {memories[0].get('response')}"
        
        result = search_web(query)
        return result
    except Exception as e:
        return f"Information retrieval error: {e}"


class SmartAgent:
    """
    Multi-step task execution agent
    Uses Groq LLM for reasoning
    """
    
    def __init__(self):
        """Initialize smart agent"""
        self.llm = None
        self.initialized = False
        
        self._initialize()
    
    def _initialize(self):
        """Initialize Groq LLM"""
        try:
            if USE_GROQ and GROQ_API_KEY:
                self.llm = ChatGroq(
                    groq_api_key=GROQ_API_KEY,
                    model_name="mixtral-8x7b-32768",
                    temperature=0
                )
                self.initialized = True
                if DEBUG_MODE:
                    print("✅ Smart agent initialized with Groq LLM")
            else:
                if DEBUG_MODE:
                    print("⚠️  Groq not configured. Running in simplified mode.")
                self.initialized = False
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Agent initialization error: {e}")
            self.initialized = False
    
    def execute_task(self, task_description: str) -> str:
        """
        Execute multi-step task
        
        Args:
            task_description: What to accomplish
        
        Returns:
            Task result
        """
        try:
            if not self.initialized:
                return self._fallback_execute(task_description)
            
            if DEBUG_MODE:
                print(f"🤖 Agent executing: {task_description}")
            
            # Create simple messages for LLM
            system_message = """You are Jarvis, an intelligent AI assistant. 
Break down complex tasks into steps and provide actionable responses.
Be concise and direct."""
            
            # Get LLM response
            messages = [
                ("system", system_message),
                ("human", task_description)
            ]
            
            response = self.llm.invoke(messages)
            result = response.content
            
            # Save to memory
            save_memory(task_description, result, memory_type="agent_task")
            
            return result
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Task execution error: {e}")
            return self._fallback_execute(task_description)
    
    def _fallback_execute(self, task: str) -> str:
        """Fallback execution without LLM"""
        task_lower = task.lower()
        
        if any(word in task_lower for word in ['search', 'find', 'look up']):
            query = task.replace('search', '').replace('find', '').replace('look up', '').strip()
            return search_web(query)
        
        elif any(word in task_lower for word in ['report', 'generate', 'create']):
            if 'fintech' in task_lower:
                return generate_report_task("fintech")
            return "Report generation requires configuration"
        
        elif any(word in task_lower for word in ['open', 'launch', 'start']):
            app = task.replace('open', '').replace('launch', '').replace('start', '').strip()
            return execute_system_task(f"open {app}")
        
        elif any(word in task_lower for word in ['what', 'how', 'when', 'where', 'why']):
            return get_information(task)
        
        else:
            return f"Task acknowledged: {task}. Enable Groq API for advanced reasoning (set GROQ_API_KEY)."


# Global agent instance
_agent = None

def get_agent():
    """Get global smart agent instance"""
    global _agent
    if _agent is None:
        _agent = SmartAgent()
    return _agent


def execute_smart_task(task_description: str) -> str:
    """Execute task with smart agent"""
    agent = get_agent()
    return agent.execute_task(task_description)

