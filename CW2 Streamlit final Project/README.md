## Multi-Domain Intelligence Platform

A comprehensive Streamlit-based application that integrates Cybersecurity, Data Science, and IT Operations with AI-powered analytics.

## Overview
 
This platform solves critical domain-specific problems through integrated analytics and AI assistance:

## Domain Problems Addressed:**
1. **Cybersecurity**: Identifies phishing spikes and response bottlenecks in incident management
2. **Data Science**: Manages dataset governance, quality, and resource consumption
3. **IT Operations**: Analyzes service desk performance and identifies process inefficiencies

## Architecture

PROJECT_ROOT/

├── .streamlit/ # Streamlit configuration
│ └── secrets.toml # API keys and secrets 

├── DATA/ # Database and data files

│ └── intelligence.db # SQLite database

├── models/ # Data models (OOP classes)
│ ├── init.py
│ ├── dataset.py # Dataset entity with quality metrics
│ ├── it_ticket.py # IT ticket with performance tracking
│ ├── security_incident.py # Security incident with threat analysis
│ └── user.py # User management

├── pages/ # Streamlit application pages
│ ├── 0_🏠_Dashboard.py # Unified multi-domain dashboard
│ ├── 1_🔐_Login.py # Authentication page
│ ├── 2_🛡_Cybersecurity.py # Cybersecurity incident management
│ ├── 3_📊_Data_Science.py # Data analytics and visualization
│ ├── 4_💻_IT_Operations.py # IT operations and AI analyzer
│ └── 5_🤖_AI_Assistant.py # AI chat assistant

├── services/ # Business logic layer
│ ├── init.py
│ ├── ai_assistant.py # OpenAI GPT integration
│ ├── auth_manager.py # Authentication and user management
│ └── database_manager.py # Database operations

├── utils/ # Utility functions
│ ├── init.py
│ ├── auth.py #Only for reference 
│ └── database.py #Only for reference
├── .env # Environment variables 
├── .gitignore # Git ignore 
├── Home.py # Main application entry point
├── README.md # This file
├── requirements.txt # Python dependencies
└── setup_db.py # Database initialization script

#Initialize the database with simple data
pyhtomn setup_db.py

To run the application, open Home.py, open terminal, and run streamlit run Home.py.

Features of this platform include Unified Dashboard, Cybersecurity, DataScience, IT Operations, AI Assistant, and Domain-Specific Problem Solving, with Object-Oriented Design. You have AI Integration, User Roles, Authentication, and Analytics and Visualization.

