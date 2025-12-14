"""AI Assistant service class"""
from typing import List, Dict, Optional
import openai

class AIAssistant:
    """Wrapper around OpenAI API for AI assistant functionality."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
        self._history: List[Dict[str, str]] = []
        self._system_prompt = "You are a helpful assistant for my Multi-Domain Intelligence Platform."
        self.client = None
        
        if api_key:
            self.set_api_key(api_key)
    
    #Configuration methods
    def set_system_prompt(self, prompt: str):
        """Set the system prompt for the AI."""
        self._system_prompt = prompt
    
    def set_api_key(self, api_key: str):
        """Set the OpenAI API key."""
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    #Messaging Methods
    def send_message(self, user_message: str, context: str = "", 
                    temperature: float = 0.7, stream: bool = False):
        """Send a message to the AI and get response."""
        if not self.client:
            return "Error: OpenAI client not configured."
        
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": self._system_prompt}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"Context: {context}"})
            
            # Add conversation history (last 10 messages)
            for msg in self._history[-10:]:
                messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            if stream:
                # For streaming responses
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=True
                )
                return response
            else:
                # For regular responses
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=500
                )
                
                ai_response = response.choices[0].message.content
                
                # Update history
                self._history.append({"role": "user", "content": user_message})
                self._history.append({"role": "assistant", "content": ai_response})
                
                return ai_response
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    #Domain-specific Analysis Methods
    def analyze_security_incident(self, incident_description: str) -> str:
        """Analyze a security incident."""
        prompt = f"""As a cybersecurity expert, analyze this security incident:

{incident_description}

Please provide:
1. Provide assessment of severity
2. Immediate actions needed
3. Long-term prevention strategies
4. Compliance considerations
5. Incident response bottlenecks by identifying phishing surges and analyzing resolution times.

Format with clear sections and bullet points."""
        return self.send_message(prompt)
    
    def analyze_dataset(self, dataset_info: str) -> str:
        """Analyze a dataset for data science insights."""
        prompt = f"""As a data management expert, analyze this dataset:

{dataset_info}

Provide insights on:
1. Provide assessment of data quality and completeness
2. Provide potential use cases
3. Provide security and privacy considerations
4. Provide integration opportunities

Format with clear sections and actionable insights."""
        return self.send_message(prompt)
    
    def analyze_it_ticket(self, ticket_info: str) -> str:
        """Generate a response for an IT ticket."""
        prompt = f"""As an IT service management expert, analyze this support ticket:

{ticket_info}

Provide analysis covering:
1. Common issue patterns
2. Provide Resolution effectiveness
3. Provide Priority accuracy assessment
4. Process bottlenecks

Format with clear sections and actionable recommendations."""
        return self.send_message(prompt)
    
    def analyze_users(self, users_info: str) -> str:
        """Analyze user accounts."""
        prompt = f"""As a security and user management expert, analyze these user accounts:

{users_info}

Provide analysis covering:
1. Role distribution
2. Access control considerations
3. Security implications
4. User management recommendations
5. Compliance considerations

Format with clear sections and actionable insights."""
        return self.send_message(prompt)
    
    #History Methods
    def clear_history(self):
        """Clear conversation history."""
        self._history.clear()
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self._history.copy()