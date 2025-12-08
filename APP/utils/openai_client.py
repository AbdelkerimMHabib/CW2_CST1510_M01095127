import streamlit as st
from openai import OpenAI
import json
from typing import Dict, List, Optional

class OpenAIClient:
    """Utility class for OpenAI API operations"""
    
    def __init__(self):
        try:
            self.client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
            self.available = True if st.secrets.get("OPENAI_API_KEY") else False
        except:
            self.available = False
    
    def analyze_cyber_incident(self, incident_data: Dict) -> str:
        """Analyze a cyber incident using AI"""
        if not self.available:
            return "OpenAI API not configured. Please add OPENAI_API_KEY to .streamlit/secrets.toml"
        
        prompt = f"""
        Analyze this cyber security incident:
        
        Title: {incident_data.get('title', 'N/A')}
        Severity: {incident_data.get('severity', 'N/A')}
        Status: {incident_data.get('status', 'N/A')}
        Date: {incident_data.get('date', 'N/A')}
        
        Provide:
        1. Risk assessment (Low/Medium/High/Critical)
        2. Recommended immediate actions
        3. Long-term mitigation strategies
        4. Compliance considerations
        5. Estimated time to resolution
        
        Format the response professionally with clear sections.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert with 15 years of experience in incident response and threat analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in AI analysis: {str(e)}"
    
    def analyze_it_ticket(self, ticket_data: Dict) -> str:
        """Analyze an IT ticket using AI"""
        if not self.available:
            return "OpenAI API not configured. Please add API key to secrets.toml"
        
        prompt = f"""
        Analyze this IT support ticket:
        
        Title: {ticket_data.get('title', 'N/A')}
        Priority: {ticket_data.get('priority', 'N/A')}
        Status: {ticket_data.get('status', 'N/A')}
        Created Date: {ticket_data.get('created_date', 'N/A')}
        
        Provide:
        1. Likely root causes (list top 3)
        2. Step-by-step troubleshooting guide
        3. Estimated resolution time
        4. Required tools or permissions
        5. Prevention tips for future occurrences
        
        Format as a structured troubleshooting guide.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an IT support expert with 10 years of experience in enterprise IT support."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in AI analysis: {str(e)}"
    
    def generate_dashboard_insights(self, metrics: Dict) -> str:
        """Generate insights from dashboard metrics"""
        if not self.available:
            return "OpenAI API not configured. Please add API key to secrets.toml"
        
        prompt = f"""
        Analyze these dashboard metrics from a multi-domain intelligence platform:
        
        CYBERSECURITY DOMAIN:
        - Total incidents: {metrics.get('incidents', 0)}
        - Open incidents: {metrics.get('open_incidents', 0)}
        - Severity distribution: {metrics.get('severity_distribution', {})}
        
        DATASETS DOMAIN:
        - Total datasets: {metrics.get('datasets', 0)}
        - Total size: {metrics.get('total_size_mb', 0)} MB
        
        IT OPERATIONS DOMAIN:
        - Total tickets: {metrics.get('tickets', 0)}
        - Open tickets: {metrics.get('open_tickets', 0)}
        - Priority distribution: {metrics.get('priority_distribution', {})}
        
        ORGANIZATION:
        - Total users: {metrics.get('users', 0)}
        
        Provide an executive summary with:
        1. Overall health assessment (Good/Concerning/Critical)
        2. Top 3 areas requiring attention
        3. Key performance indicators to monitor
        4. Recommended actions for each domain
        5. Risk level assessment
        
        Format as a professional executive briefing.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business intelligence analyst with expertise in multi-domain platform analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def chat(self, messages: List[Dict], model: str = "gpt-4o", 
             temperature: float = 0.7, max_tokens: int = 1000,
             stream: bool = False):
        """Generic chat completion"""
        if not self.available:
            return None
        
        try:
            if stream:
                return self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
            else:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
        except Exception as e:
            return f"Error in chat completion: {str(e)}"
    
    def summarize_text(self, text: str, max_length: int = 500) -> str:
        """Summarize text using AI"""
        if not self.available:
            return text[:max_length] + "..." if len(text) > max_length else text
        
        prompt = f"Summarize this text in under {max_length} characters:\n\n{text}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a concise summarizer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return text[:max_length] + "..." if len(text) > max_length else text

# Global instance
openai_client = OpenAIClient()