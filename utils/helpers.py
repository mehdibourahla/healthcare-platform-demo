import logging
import streamlit as st
from typing import Optional
from qdrant_client import QdrantClient

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def initialize_qdrant_client(host: str, port: int, api_key: str = None):
    """Initialize Qdrant client for cloud deployment"""
    try:
        if api_key:
            client = QdrantClient(
                url=host,
                api_key=api_key,
            )
        else:  # Local deployment
            client = QdrantClient(host=host, port=port)
        
        client.get_collections()  # Test connection
        return client
    except Exception as e:
        st.warning(f"Qdrant connection failed: {e}. Using fallback mode.")
        return None

def validate_openai_key(api_key: str) -> bool:
    """Validate OpenAI API key"""
    if not api_key:
        st.error("Please set OPENAI_API_KEY environment variable")
        return False
    return True

def clear_session_state():
    """Clear all demo-related session state"""
    keys_to_clear = [
        "current_patient", "current_assessment", "triage_result", 
        "mock_triage", "physician_recommendations", "selected_physician",
        "appointment_confirmed", "demo_mode", "use_demo_data"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def format_medical_list(items: list, max_items: int = 3) -> str:
    """Format a list of medical items for display"""
    if not items:
        return "None"
    
    if len(items) <= max_items:
        return ", ".join(items)
    else:
        return f"{', '.join(items[:max_items])}, and {len(items) - max_items} more"

def get_urgency_color(urgency_level: str) -> str:
    """Get color code for urgency level"""
    colors = {
        "Critical Emergency": "🔴",
        "Urgent": "🟠", 
        "Semi-Urgent": "🟡",
        "Standard": "🟢",
        "Non-Urgent": "🔵"
    }
    return colors.get(urgency_level, "⚪")

def calculate_age_group(age: int) -> str:
    """Calculate age group for medical context"""
    if age < 2:
        return "Infant"
    elif age < 12:
        return "Child"
    elif age < 18:
        return "Adolescent"
    elif age < 65:
        return "Adult"
    else:
        return "Elderly"

def format_phone_number(phone: str) -> str:
    """Format phone number for display"""
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default