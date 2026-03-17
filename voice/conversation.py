# Conversation Mode - Two-way voice dialogue between human and Jarvis

from voice.listen import listen
from voice.speak import speak
from brain.agent import think
from config import DEBUG_MODE, ASSISTANT_NAME
import time

class ConversationMode:
    """
    Interactive two-way conversation with voice
    Jarvis listens, responds, listens again - like talking to a friend
    """
    
    def __init__(self):
        self.running = False
        self.conversation_history = []
        self.turn_count = 0
    
    def start_conversation(self):
        """
        Start interactive voice conversation mode
        """
        self.running = True
        self.conversation_history = []
        self.turn_count = 0
        
        print("\n" + "="*70)
        print("[🎯 CONVERSATION MODE]")
        print("="*70)
        print("Now talking with Jarvis in real-time conversation!")
        print("Just speak naturally - Jarvis will respond and keep talking.")
        print("Say 'exit conversation' to end the chat.")
        print("="*70 + "\n")
        
        speak(f"Welcome to conversation mode! I'm {ASSISTANT_NAME}. What would you like to talk about?")
        print(f"🤖 {ASSISTANT_NAME}: Welcome to conversation mode! I'm {ASSISTANT_NAME}. What would you like to talk about?\n")
        
        # Start the conversation loop
        self.conversation_loop()
    
    def conversation_loop(self):
        """
        Main conversation loop - back and forth dialogue
        """
        greetings = [
            "That's interesting! Tell me more.",
            "I see! Continue please.",
            "Go ahead, I'm listening.",
            "And then what happened?",
            "That sounds great! What else?",
            "Interesting point! Anything else?",
            "I understand. Please go on.",
        ]
        
        greeting_index = 0
        
        while self.running:
            self.turn_count += 1
            
            print(f"\n[TURN {self.turn_count}] Your turn - speak now:")
            speak("Your turn, speak now")
            
            # Listen to user input
            user_message = listen(timeout=10, phrase_time_limit=15)
            
            if not user_message:
                speak("Sorry, I didn't catch that. Can you repeat?")
                print("❌ No input detected. Please try again.\n")
                continue
            
            # Check for exit commands
            if self._is_exit_command(user_message):
                self._end_conversation()
                break
            
            # Store in history
            self.conversation_history.append({"role": "user", "message": user_message})
            print(f"\n👤 You: {user_message}")
            
            # Get AI response
            print(f"\n🤖 {ASSISTANT_NAME}: Thinking...", end="")
            jarvis_response = self._get_conversation_response(user_message)
            print("\r" + " "*50 + "\r", end="")  # Clear "Thinking..."
            
            if jarvis_response:
                print(f"🤖 {ASSISTANT_NAME}: {jarvis_response}")
                speak(jarvis_response)
                self.conversation_history.append({"role": "assistant", "message": jarvis_response})
            else:
                speak("Hmm, I'm having trouble understanding. Can you rephrase that?")
                print(f"🤖 {ASSISTANT_NAME}: Hmm, I'm having trouble understanding. Can you rephrase that?")
            
            # Add a prompt for continuation
            greeting_index = (greeting_index + 1) % len(greetings)
            print(f"\n💬 {greetings[greeting_index]}\n")
            time.sleep(1)  # Small pause between exchanges
    
    def _get_conversation_response(self, user_message):
        """
        Get Jarvis response using AI reasoning
        """
        try:
            # Build context from conversation history
            history_text = ""
            if len(self.conversation_history) > 2:
                # Include last 2 exchanges for context
                recent = self.conversation_history[-4:]
                for msg in recent:
                    role = "User" if msg["role"] == "user" else ASSISTANT_NAME
                    history_text += f"{role}: {msg['message']}\n"
            
            # Create an enhanced prompt with context
            context = f"""You are {ASSISTANT_NAME}, a friendly and conversational AI assistant.
            
Keep responses natural, engaging, and concise (2-3 sentences max).
Be conversational - like talking to a friend.
Ask follow-up questions when appropriate.

Recent conversation:
{history_text}

User's latest message: {user_message}

Respond naturally and conversationally:"""
            
            response = think(context)
            return response
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Conversation response error: {e}")
            return None
    
    def _is_exit_command(self, message):
        """
        Check if user wants to exit conversation
        """
        exit_phrases = [
            'exit conversation',
            'exit',
            'quit',
            'bye',
            'goodbye',
            'end conversation',
            'stop conversation',
            'thanks bye',
            'see you later',
            'end chat'
        ]
        return message.lower() in exit_phrases or any(exit_phrase in message.lower() for exit_phrase in exit_phrases)
    
    def _end_conversation(self):
        """
        End the conversation gracefully
        """
        self.running = False
        
        print("\n" + "="*70)
        print(f"[CONVERSATION SUMMARY]")
        print(f"Turns: {self.turn_count}")
        print(f"Total exchanges: {len(self.conversation_history)}")
        print("="*70)
        
        speak(f"Thank you for the conversation! See you next time")
        print(f"🤖 {ASSISTANT_NAME}: Thank you for the conversation! See you next time.\n")
    
    def get_conversation_summary(self):
        """
        Get a summary of the conversation
        """
        summary = {
            "turns": self.turn_count,
            "total_messages": len(self.conversation_history),
            "history": self.conversation_history
        }
        return summary


def start_conversation_mode():
    """
    Entry point for conversation mode
    """
    conversation = ConversationMode()
    conversation.start_conversation()
