# app.py - Main Healthcare Platform Demo Application

import streamlit as st
import openai

# Import configuration
from config import (
    QDRANT_HOST, QDRANT_PORT, OPENAI_API_KEY, STREAMLIT_CONFIG
)

# Import core systems
from core import MedicalKnowledgeRAG, MedicalContextEngineer, MedicalAgentSystem

# Import UI components
from ui import (
    show_workflow_progress, get_current_step, show_demo_controls, 
    show_quick_actions, show_error_page, HealthcarePlatformPages,
    SymptomPages, PhysicianPages
)

# Import utilities
from utils import (
    setup_logging, initialize_qdrant_client, validate_openai_key
)

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

class HealthcarePlatformDemo:
    """Main healthcare platform demo application"""
    
    def __init__(self):
        """Initialize the healthcare platform demo"""
        self.qdrant_client = None
        self.rag_system = None
        self.context_engineer = None
        self.agent_system = None
        
        # Initialize UI page handlers
        self.main_pages = HealthcarePlatformPages(self)
        self.symptom_pages = SymptomPages(self)
        self.physician_pages = PhysicianPages(self)
        
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Initialize all healthcare platform systems"""
        try:
            # Setup logging
            setup_logging()
            
            # Validate OpenAI API key
            if not validate_openai_key(OPENAI_API_KEY):
                st.stop()
            
            # Initialize Qdrant client
            self.qdrant_client = initialize_qdrant_client(QDRANT_HOST, QDRANT_PORT)
            
            # Initialize core systems
            self.rag_system = MedicalKnowledgeRAG(self.qdrant_client)
            self.context_engineer = MedicalContextEngineer()
            self.agent_system = MedicalAgentSystem(self.rag_system, self.context_engineer)
            
            print("✅ Healthcare platform systems initialized successfully")
            
        except Exception as e:
            st.error(f"System initialization failed: {e}")
            # Initialize fallback systems
            self.rag_system = MedicalKnowledgeRAG(None)
            self.context_engineer = MedicalContextEngineer() 
            self.agent_system = MedicalAgentSystem(self.rag_system, self.context_engineer)
    
    def run(self):
        """Run the Streamlit application"""
        # Configure Streamlit page
        st.set_page_config(**STREAMLIT_CONFIG)
        
        # Set page title and description
        st.title("🏥 Intelligent Healthcare Platform Demo")
        st.markdown("*Demonstrating RAG, Agentic AI, and Context Engineering in Healthcare*")
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        
        # Show current step in the workflow
        current_step = get_current_step()
        if current_step:
            st.sidebar.info(f"Current Step: {current_step}")
        
        # Main navigation menu
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["🏠 Overview", "👤 Patient Registration", "🩺 Symptom Assessment", 
             "🧠 AI Triage System", "👨‍⚕️ Physician Matching", "📅 Appointment Scheduling", 
             "📊 System Analytics", "🔧 Architecture Demo"]
        )
        
        # Show workflow progress
        show_workflow_progress()
        
        # Demo controls
        show_demo_controls()
        
        # Quick actions
        show_quick_actions()
        
        # Route to appropriate page with error handling
        try:
            self._route_to_page(page)
        except Exception as e:
            show_error_page(str(e), f"Page: {page}")
    
    def _route_to_page(self, page: str):
        """Route to the appropriate page based on selection"""
        if page == "🏠 Overview":
            self.main_pages.show_overview()
        elif page == "👤 Patient Registration":
            self.main_pages.show_patient_registration()
        elif page == "🩺 Symptom Assessment":
            self.symptom_pages.show_symptom_assessment()
        elif page == "🧠 AI Triage System":
            self.symptom_pages.show_ai_triage()
        elif page == "👨‍⚕️ Physician Matching":
            self.physician_pages.show_physician_matching()
        elif page == "📅 Appointment Scheduling":
            self.physician_pages.show_appointment_scheduling()
        elif page == "📊 System Analytics":
            self.main_pages.show_system_analytics()
        elif page == "🔧 Architecture Demo":
            self.main_pages.show_architecture_demo()
        else:
            st.error(f"Unknown page: {page}")

def main():
    """Main application entry point"""
    # Initialize and run the healthcare platform demo
    app = HealthcarePlatformDemo()
    app.run()

if __name__ == "__main__":
    main()