from openai import OpenAI
from typing import List, Dict, Optional
import streamlit as st
import os

class AIAssistant:
    """AI ANALYZER - Core AI integration for multi-domain analysis"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or self._get_api_key()
        self.model = model
        self.client = self._initialize_client()
    
    def _get_api_key(self) -> Optional[str]:
        try:
            if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
                return st.secrets["OPENAI_API_KEY"]
        except:
            pass
        return os.getenv("OPENAI_API_KEY")
    
    def _initialize_client(self) -> Optional[OpenAI]:
        if not self.api_key:
            st.warning("OpenAI API key not configured.")
            return None
        try:
            return OpenAI(api_key=self.api_key)
        except Exception:
            return None
    
    def is_available(self) -> bool:
        return self.client is not None
    
    # ============ CYBERSECURITY ANALYSIS ============
    def analyze_security_incidents(self, incidents: List[Dict], analysis_type: str = "Comprehensive Analysis") -> str:
        """AI Analyzer for Security Incidents"""
        if not self.is_available():
            return "AI Assistant is not available."
        
        try:
            incidents_text = "\n\n".join([
                f"Incident {i+1}:\n"
                f"- Title: {inc['title']}\n"
                f"- Severity: {inc['severity']}\n"
                f"- Status: {inc['status']}\n"
                f"- Date: {inc['date']}"
                for i, inc in enumerate(incidents)
            ])
            
            prompt = f"""As a cybersecurity expert, analyze these incidents:

{incidents_text}

Analysis Type: {analysis_type}

Provide analysis including:
1. Overall risk assessment
2. Common patterns or trends
3. Immediate actions needed
4. Long-term prevention strategies
5. Recommendations for each incident

Format with clear sections and bullet points."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior cybersecurity analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ============ DATASET ANALYSIS ============
    def analyze_datasets(self, datasets: List[Dict], analysis_type: str = "Data Quality Assessment") -> str:
        """AI Analyzer for Datasets"""
        if not self.is_available():
            return "AI Assistant is not available."
        
        try:
            datasets_text = "\n\n".join([
                f"Dataset {i+1}:\n"
                f"- Name: {ds['name']}\n"
                f"- Source: {ds['source']}\n"
                f"- Category: {ds['category']}\n"
                f"- Size: {ds['size']} MB"
                for i, ds in enumerate(datasets)
            ])
            
            prompt = f"""As a data management expert, analyze:

{datasets_text}

Analysis Type: {analysis_type}

Provide insights on:
1. Data quality and completeness
2. Potential use cases
3. Security and privacy considerations
4. Integration opportunities
5. Recommendations for data governance

Format with clear sections."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data architect and governance expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ============ IT TICKET ANALYSIS ============
    def analyze_it_tickets(self, tickets: List[Dict], analysis_type: str = "Support Trends") -> str:
        """AI Analyzer for IT Tickets"""
        if not self.is_available():
            return "AI Assistant is not available."
        
        try:
            tickets_text = "\n\n".join([
                f"Ticket {i+1}:\n"
                f"- Title: {ticket['title']}\n"
                f"- Priority: {ticket['priority']}\n"
                f"- Status: {ticket['status']}\n"
                f"- Created: {ticket['created_date']}"
                for i, ticket in enumerate(tickets)
            ])
            
            prompt = f"""As an IT service management expert, analyze:

{tickets_text}

Analysis Type: {analysis_type}

Provide analysis covering:
1. Common issue patterns
2. Resolution effectiveness
3. Priority accuracy assessment
4. Process bottlenecks
5. Recommendations for IT service improvement

Format with clear sections."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an ITIL certified service management expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ============ GENERAL CHAT ============
    def chat_completion(self, messages: List[Dict], system_prompt: str = None, temperature: float = 0.7) -> Optional[str]:
        if not self.is_available():
            return None
        
        try:
            all_messages = []
            if system_prompt:
                all_messages.append({"role": "system", "content": system_prompt})
            all_messages.extend(messages)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=all_messages,
                temperature=temperature,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception:
            return None