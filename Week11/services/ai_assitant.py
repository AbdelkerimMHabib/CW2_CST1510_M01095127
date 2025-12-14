# 3.3 AIAssistant (services/ai_assistant.py)

from typing import List, Dict, Optional

class AIAssistant:
    """Simple wrapper around an AI/chat model.
    
    In your real project, connect this to OpenAI or another provider.
    """
    
    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []
    
    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for the assistant."""
        self._system_prompt = prompt
    
    def send_message(self, user_message: str) -> str:
        """Send a message and get a (fake) response.
        
        Replace this body with your real API call.
        """
        self._history.append({"role": "user", "content": user_message})
        # Fake response for now:
        response = f"[AI reply to]: {user_message[:50]}..."
        self._history.append({"role": "assistant", "content": response})
        return response
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._history.clear()
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self._history.copy()
    
    def get_system_prompt(self) -> str:
        """Get the current system prompt."""
        return self._system_prompt