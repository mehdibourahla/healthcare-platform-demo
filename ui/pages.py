import streamlit as st
import pandas as pd
import datetime
import uuid
import time
import asyncio
from typing import Dict, List

from models import Patient, SymptomAssessment, TriageResult, PhysicianRecommendation, UrgencyLevel
from config import DEMO_PATIENT_DATA, DEMO_SYMPTOMS_DATA
from .components import show_rag_demo_section

class HealthcarePlatformPages:
    def __init__(self, app_instance):
        self.app = app_instance
    
    def show_overview(self):
        """Show platform overview"""
        st.header("Healthcare Platform Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Platform Capabilities")
            st.write("""
            **Intelligent Patient Triage:**
            - AI-powered symptom assessment
            - Evidence-based medical reasoning
            - Real-time risk stratification
            
            **Smart Physician Matching:**
            - Specialty-based recommendations
            - Insurance and location optimization
            - Availability coordination
            
            **Automated Care Coordination:**
            - End-to-end workflow management
            - Multi-agent collaboration
            - Continuous care monitoring
            """)
        
        with col2:
            st.subheader("🏗️ Architecture Components")
            st.write("""
            **RAG System (Core Intelligence):**
            - Medical knowledge retrieval from 50+ protocols
            - Semantic search across clinical guidelines
            - Real-time evidence-based recommendations
            - Patient-specific contextualization
            
            **Agentic AI (Workflow Orchestration):**
            - Multi-step medical reasoning
            - Workflow orchestration across specialties
            - Emergency detection and escalation
            - Care coordination automation
            
            **Context Engineering (Patient Intelligence):**
            - Comprehensive patient modeling
            - Risk factor analysis and validation
            - Temporal medical reasoning
            - Social determinant integration
            """)
            
            # Show RAG in action stats
            st.info("🔍 **RAG Powers Every Decision**: Each triage retrieves 3-5 relevant medical protocols, ensuring evidence-based care recommendations.")
            
            # Mini RAG demo
            with st.expander("🧪 See RAG in Action"):
                st.write("**Example: Chest Pain Query**")
                st.code("Query: 'chest pain shortness of breath exertion'")
                st.write("**RAG Retrieves:**")
                st.write("📄 Chest Pain Assessment Protocol (0.89 similarity)")
                st.write("📄 Acute Coronary Syndrome Guidelines (0.86 similarity)")  
                st.write("📄 Cardiac Risk Stratification (0.83 similarity)")
                st.write("**Result:** → Cardiology referral recommended")
        
        st.subheader("🚀 Demo Workflow")
        st.write("""
        1. **Patient Registration**: Create comprehensive medical profile (pre-filled available)
        2. **Symptom Assessment**: AI-powered symptom gathering and analysis (cardiac scenario ready)
        3. **Intelligent Triage**: RAG + Context + Agents working together
        4. **Physician Matching**: Smart specialty and preference matching
        5. **Appointment Coordination**: Automated scheduling and preparation
        """)
        
        # Demo scenario info
        st.subheader("🎬 Available Demo Scenarios")
        
        scenarios = {
            "cardiac": {
                "name": "Cardiac Risk Assessment", 
                "icon": "🫀",
                "description": "52-year-old with chest pain and multiple cardiac risk factors",
                "highlights": ["RAG retrieves chest pain protocols", "High-risk context analysis", "Cardiology referral pathway"]
            },
            "emergency": {
                "name": "Emergency Detection",
                "icon": "🚨", 
                "description": "Severe symptoms triggering emergency protocols",
                "highlights": ["Emergency escalation demo", "911 integration", "Critical pathway activation"]
            },
            "routine": {
                "name": "Routine Care",
                "icon": "👩‍⚕️",
                "description": "General wellness check with minor concerns", 
                "highlights": ["Standard triage workflow", "General medicine referral", "Non-urgent scheduling"]
            }
        }
        
        cols = st.columns(3)
        
        for i, (key, scenario) in enumerate(scenarios.items()):
            with cols[i]:
                st.markdown(f"### {scenario['icon']} {scenario['name']}")
                st.write(scenario['description'])
                for highlight in scenario['highlights']:
                    st.write(f"• {highlight}")
                
                if key == "cardiac":
                    st.success("👆 **Default Demo Scenario**")
        
        with st.expander("📋 Cardiac Scenario Details (Default)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Patient Profile:**")
                st.write("• 52-year-old Hispanic male")
                st.write("• Location: Boston, MA") 
                st.write("• Insurance: Blue Cross")
                st.write("• Medical History: Hypertension, Diabetes")
                st.write("• Family History: Heart Disease, Diabetes")
                st.write("• Medications: Lisinopril, Metformin, Atorvastatin")
                st.write("• Lifestyle: Former smoker, moderate stress")
            
            with col2:
                st.write("**Presenting Symptoms:**")
                st.write("• Chest pain/pressure with exertion")
                st.write("• Shortness of breath")
                st.write("• Fatigue and sweating")
                st.write("• Pain radiating to left arm")
                st.write("• Symptoms worsen with activity")
                st.write("• Relieved by rest")
                st.write("• Duration: 1-4 weeks, severity 6/10")
                
        st.write("**Why this scenario is perfect for the demo:**")
        st.write("✅ Multiple cardiac risk factors trigger advanced risk assessment")
        st.write("✅ Symptoms clearly indicate cardiology referral")  
        st.write("✅ RAG system will retrieve relevant chest pain protocols")
        st.write("✅ Context engineering will identify high-risk patient profile")
        st.write("✅ Agentic AI will coordinate appropriate urgent care")
        st.write("✅ Shows emergency detection vs. urgent care pathways")
        
        # Quick demo buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎬 Start Quick Demo with Pre-filled Data", type="primary"):
                st.session_state.demo_mode = True
                st.session_state.use_demo_data = True
                st.success("✅ Demo mode activated! Forms will be pre-filled.")
                st.info("👆 Click 'Patient Registration' in the sidebar to begin!")
        
        with col2:
            if st.button("🎯 Start Custom Demo", type="secondary"):
                st.session_state.demo_mode = True
                st.session_state.use_demo_data = False
                st.info("👆 Click 'Patient Registration' in the sidebar to begin with empty forms!")

    def show_patient_registration(self):
        """Show patient registration interface"""
        st.header("👤 Patient Registration & Profile Creation")
        
        # Add demo data toggle
        demo_mode = st.session_state.get("demo_mode", False)
        use_demo_data = st.checkbox("🎬 Use Demo Data (Pre-filled for easy demonstration)", 
                                   value=demo_mode or st.session_state.get("use_demo_data", True))
        
        if use_demo_data:
            st.info("📋 **Demo Patient: Robert Martinez** - 52-year-old with cardiac risk factors")
        
        with st.form("patient_registration"):
            st.subheader("Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*", 
                    value=DEMO_PATIENT_DATA["name"] if use_demo_data else "", 
                    placeholder="John Doe")
                age = st.number_input("Age*", min_value=0, max_value=150, 
                    value=DEMO_PATIENT_DATA["age"] if use_demo_data else 35)
                gender = st.selectbox("Gender*", 
                    ["Male", "Female", "Other", "Prefer not to say"],
                    index=0 if use_demo_data else 0)
                phone = st.text_input("Phone*", 
                    value=DEMO_PATIENT_DATA["phone"] if use_demo_data else "",
                    placeholder="+1 (555) 123-4567")
            
            with col2:
                email = st.text_input("Email*", 
                    value=DEMO_PATIENT_DATA["email"] if use_demo_data else "",
                    placeholder="john.doe@email.com")
                location = st.text_input("Location*", 
                    value=DEMO_PATIENT_DATA["location"] if use_demo_data else "",
                    placeholder="New York, NY")
                insurance = st.selectbox("Insurance Provider*", 
                    ["Aetna", "Blue Cross", "Cigna", "UnitedHealth", "Medicare", "Medicaid", "Other"],
                    index=1 if use_demo_data else 0)  # Blue Cross
                emergency_contact = st.text_input("Emergency Contact", 
                    value=DEMO_PATIENT_DATA["emergency_contact"] if use_demo_data else "",
                    placeholder="Jane Doe - (555) 987-6543")
            
            st.subheader("Medical History")
            col1, col2 = st.columns(2)
            
            with col1:
                medical_history = st.multiselect(
                    "Chronic Conditions",
                    ["Diabetes", "Hypertension", "Heart Disease", "Asthma", "Cancer", 
                     "Kidney Disease", "Liver Disease", "Mental Health Conditions", "Other"],
                    default=DEMO_PATIENT_DATA["medical_history"] if use_demo_data else []
                )
                
                allergies = st.multiselect(
                    "Allergies",
                    ["Penicillin", "Sulfa", "Aspirin", "Latex", "Shellfish", "Nuts", "Other"],
                    default=DEMO_PATIENT_DATA["allergies"] if use_demo_data else []
                )
            
            with col2:
                current_medications = st.text_area(
                    "Current Medications",
                    value="\n".join(DEMO_PATIENT_DATA["current_medications"]) if use_demo_data else "",
                    placeholder="List all current medications, dosages, and frequency"
                )
                
                family_history = st.multiselect(
                    "Family Medical History",
                    ["Heart Disease", "Cancer", "Diabetes", "Stroke", "Mental Health", "Other"],
                    default=DEMO_PATIENT_DATA["family_history"] if use_demo_data else []
                )
            
            st.subheader("Lifestyle Factors")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                smoking = st.selectbox("Smoking Status", 
                    ["Never", "Former", "Current"],
                    index=1 if use_demo_data else 0)  # Former
                alcohol = st.selectbox("Alcohol Use", 
                    ["None", "Occasional", "Regular", "Heavy"],
                    index=1 if use_demo_data else 0)  # Occasional
            
            with col2:
                exercise = st.selectbox("Exercise Frequency", 
                    ["None", "Rarely", "Weekly", "Daily"],
                    index=2 if use_demo_data else 0)  # Weekly
                diet = st.selectbox("Diet Type", 
                    ["Standard", "Vegetarian", "Vegan", "Keto", "Other"],
                    index=0 if use_demo_data else 0)  # Standard
            
            with col3:
                sleep_hours = st.number_input("Average Sleep Hours", min_value=0, max_value=24, 
                    value=DEMO_PATIENT_DATA["lifestyle_factors"]["sleep_hours"] if use_demo_data else 7)
                stress_level = st.slider("Stress Level (1-10)", 1, 10, 
                    value=DEMO_PATIENT_DATA["lifestyle_factors"]["stress_level"] if use_demo_data else 5)
            
            submitted = st.form_submit_button("Register Patient", type="primary")
            
            if submitted:
                if name and age and gender and phone and email and location and insurance:
                    # Create patient object
                    patient = Patient(
                        patient_id=str(uuid.uuid4())[:8],
                        name=name,
                        age=age,
                        gender=gender,
                        location=location,
                        phone=phone,
                        email=email,
                        insurance=insurance,
                        emergency_contact=emergency_contact,
                        medical_history=medical_history,
                        current_medications=current_medications.split('\n') if current_medications else [],
                        allergies=allergies,
                        family_history=family_history,
                        lifestyle_factors={
                            "smoking": smoking,
                            "alcohol": alcohol, 
                            "exercise": exercise,
                            "diet": diet,
                            "sleep_hours": sleep_hours,
                            "stress_level": stress_level
                        },
                        created_at=datetime.datetime.now()
                    )
                    
                    # Store in session state
                    st.session_state.current_patient = patient
                    
                    st.success(f"✅ Patient {name} registered successfully!")
                    st.success(f"🆔 Patient ID: {patient.patient_id}")
                    
                    # Show what happens in the real system
                    with st.expander("🔧 Real System Implementation"):
                        st.write("**In the production system, this would trigger:**")
                        st.code("""
print("🏥 PATIENT REGISTRATION SYSTEM:")
print("   📝 Validating patient information...")
print("   💾 Storing encrypted patient data in secure database")
print("   🔐 Creating HIPAA-compliant patient record")
print("   📧 Sending welcome email with patient portal access")
print("   🔗 Linking to insurance verification system")
print("   📱 Setting up patient communication preferences")
print("   ✅ Patient profile created successfully")
                        """, language="python")
                    
                    # Option to proceed to symptom assessment
                    if st.button("➡️ Proceed to Symptom Assessment"):
                        st.success("Click on 'Symptom Assessment' in the sidebar to continue!")
                        st.rerun()
                
                else:
                    st.error("Please fill in all required fields marked with *")

    def show_system_analytics(self):
        """Show system analytics and metrics"""
        st.header("📊 System Analytics & Performance")
        
        # Mock analytics data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Patients Triaged", "1,247", "↗️ +12%")
        
        with col2:
            st.metric("Avg. Triage Time", "2.3 min", "↘️ -15%")
        
        with col3:
            st.metric("Accuracy Rate", "94.2%", "↗️ +2%")
        
        with col4:
            st.metric("Patient Satisfaction", "4.8/5", "↗️ +0.2")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Triage Distribution")
            urgency_data = {
                "Urgency Level": ["Critical", "Urgent", "Semi-Urgent", "Standard", "Non-Urgent"],
                "Count": [23, 89, 156, 432, 547]
            }
            df = pd.DataFrame(urgency_data)
            st.bar_chart(df.set_index("Urgency Level"))
        
        with col2:
            st.subheader("🏥 Specialty Referrals") 
            specialty_data = {
                "Specialty": ["General Medicine", "Cardiology", "Dermatology", "Neurology", "Orthopedics"],
                "Referrals": [345, 189, 156, 134, 123]
            }
            df = pd.DataFrame(specialty_data)
            st.bar_chart(df.set_index("Specialty"))
        
        # System performance
        st.subheader("⚡ System Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**RAG System Performance:**")
            st.write("• Knowledge Retrieval: 98.5% accuracy")
            st.write("• Average Query Time: 0.8 seconds")
            st.write("• Vector DB Status: ✅ Operational")
            st.write("• Medical Guidelines: 50,000+ documents")
            
            # Show current knowledge base content
            with st.expander("📚 Current Knowledge Base Contents"):
                kb_contents = [
                    "Chest Pain Assessment Protocol",
                    "Headache Triage Guidelines", 
                    "Acute Abdominal Pain Protocol",
                    "Skin Lesion Assessment",
                    "Pediatric Fever Guidelines",
                    "Cardiac Emergency Protocols",
                    "Neurological Red Flags",
                    "Drug Interaction Database",
                    "Allergy Management Guidelines",
                    "Infectious Disease Protocols"
                ]
                
                for content in kb_contents:
                    st.write(f"📄 {content}")
        
        with col2:
            st.write("**AI Agent Performance:**")
            st.write("• Triage Accuracy: 94.2%") 
            st.write("• Physician Matching: 96.8% satisfaction")
            st.write("• Scheduling Success: 99.1%")
            st.write("• Emergency Detection: 100% accuracy")
            
            # Show RAG retrieval stats
            with st.expander("🔍 RAG Retrieval Statistics"):
                st.write("**Today's RAG Queries:**")
                st.write("• Chest pain protocols: 23 retrievals")
                st.write("• Headache guidelines: 15 retrievals") 
                st.write("• Abdominal pain: 12 retrievals")
                st.write("• Skin conditions: 8 retrievals")
                st.write("• Joint pain: 6 retrievals")
                
                st.write("**Most Retrieved Guidelines:**")
                st.write("1. Chest Pain Assessment Protocol (89 times)")
                st.write("2. Headache Red Flags (67 times)")
                st.write("3. Abdominal Pain Triage (45 times)")
        
        # Real-time monitoring
        st.subheader("📡 Real-time Monitoring")
        
        monitoring_data = {
            "Component": ["API Gateway", "Vector Database", "AI Models", "Scheduling Service", "Notification Service"],
            "Status": ["✅ Healthy", "✅ Healthy", "⚠️ High Load", "✅ Healthy", "✅ Healthy"],
            "Response Time": ["45ms", "120ms", "850ms", "200ms", "95ms"],
            "Uptime": ["99.98%", "99.95%", "99.87%", "99.99%", "99.94%"]
        }
        
        df = pd.DataFrame(monitoring_data)
        st.dataframe(df, use_container_width=True)

    def show_architecture_demo(self):
        """Show architecture components and how they work together"""
        st.header("🔧 Architecture Demonstration")
        
        st.write("This section demonstrates how RAG, Agentic AI, and Context Engineering work together in the healthcare platform.")
        
        # Architecture overview
        st.subheader("🏗️ System Architecture")
        
        architecture_components = {
            "Component": ["RAG System", "Context Engineering", "Agentic AI", "Vector Database", "LLM Integration"],
            "Technology": ["Qdrant + OpenAI", "Python Classes", "Async Agents", "Qdrant Vector DB", "GPT-4o-mini"],
            "Purpose": ["Medical Knowledge", "Patient Context", "Workflow Orchestration", "Semantic Search", "AI Reasoning"],
            "Status": ["✅ Active", "✅ Active", "✅ Active", "✅ Connected", "✅ Connected"]
        }
        
        df = pd.DataFrame(architecture_components)
        st.dataframe(df, use_container_width=True)
        
        # Component details
        tabs = st.tabs(["🔍 RAG System", "🧠 Context Engineering", "🤖 Agentic AI", "🔧 Integration"])
        
        with tabs[0]:
            st.subheader("RAG (Retrieval-Augmented Generation)")
            
            st.write("**How it works in our platform:**")
            st.write("1. **Medical Knowledge Base**: Stores clinical guidelines, medical literature")
            st.write("2. **Semantic Search**: Finds relevant medical information based on symptoms")
            st.write("3. **Context Fusion**: Combines retrieved knowledge with patient context")
            
            st.code("""
# RAG Implementation Example
class MedicalKnowledgeRAG:
    async def retrieve_medical_knowledge(self, symptoms, patient_context):
        # Create embedding for symptoms
        query_embedding = await self.create_embedding(symptoms)
        
        # Search vector database
        results = self.qdrant_client.search(
            collection_name="medical_knowledge",
            query_vector=query_embedding,
            limit=3
        )
        
        # Return relevant medical guidelines
        return self.format_medical_knowledge(results)
            """, language="python")
            
            # Interactive RAG Demo
            show_rag_demo_section()
        
        with tabs[1]:
            st.subheader("Context Engineering")
            
            st.write("**Patient Context Components:**")
            st.write("• **Demographic**: Age, gender, location")
            st.write("• **Medical History**: Chronic conditions, medications, allergies")
            st.write("• **Current Symptoms**: Severity, duration, associated factors")
            st.write("• **Risk Assessment**: Calculated risk factors and scores")
            st.write("• **Social Determinants**: Insurance, access, preferences")
            
            st.code("""
# Context Engineering Example
class MedicalContextEngineer:
    async def build_comprehensive_context(self, patient, assessment):
        context = {
            "demographic": self.get_demographic_context(patient),
            "medical": self.get_medical_history_context(patient),
            "symptom": self.get_current_symptom_context(assessment),
            "risk": self.calculate_risk_factors(patient, assessment),
            "temporal": self.get_temporal_context(),
            "social": self.get_social_determinants(patient)
        }
        return self.validate_context_consistency(context)
            """, language="python")
            
            if st.button("🧠 Show Context Building"):
                st.write("**Building context for sample patient:**")
                st.write("✅ Demographic context: 35-year-old male")
                st.write("✅ Medical context: Hypertension, no allergies")
                st.write("✅ Symptom context: Chest pain, severity 7/10")
                st.write("✅ Risk context: 2 risk factors identified")
                st.write("✅ Context validation: Consistent")
        
        with tabs[2]:
            st.subheader("Agentic AI System")
            
            st.write("**AI Agents in the Platform:**")
            st.write("• **Triage Agent**: Performs medical assessment and risk stratification")
            st.write("• **Physician Matching Agent**: Finds optimal physicians based on criteria")
            st.write("• **Scheduling Agent**: Coordinates appointment booking")
            st.write("• **Workflow Coordinator**: Manages end-to-end patient journey")
            
            st.code("""
# Agentic AI Example
class MedicalAgentSystem:
    async def coordinate_patient_journey(self, patient, assessment):
        # Build comprehensive context
        context = await self.context_engineer.build_context(patient, assessment)
        
        # Agent 1: Triage
        triage_result = await self.triage_agent.perform_triage(
            assessment, context, self.rag_system
        )
        
        # Agent 2: Physician Matching
        physicians = await self.physician_agent.match_physicians(
            triage_result, patient, context
        )
        
        # Agent 3: Scheduling
        appointment = await self.scheduling_agent.schedule_appointment(
            patient, triage_result, physicians
        )
        
        return self.compile_results(context, triage_result, physicians, appointment)
            """, language="python")
            
            if st.button("🤖 Show Agent Coordination"):
                st.write("**Agent workflow execution:**")
                st.write("🏥 Triage Agent: Analyzing symptoms...")
                st.write("👨‍⚕️ Physician Agent: Matching specialists...")
                st.write("📅 Scheduling Agent: Booking appointment...")
                st.write("🔄 Coordinator: Finalizing care plan...")
                st.write("✅ Patient journey completed")
        
        with tabs[3]:
            st.subheader("System Integration")
            
            st.write("**How the components work together:**")
            
            integration_flow = """
            1. Patient enters symptoms
            2. Context Engineering builds comprehensive patient model
            3. RAG System retrieves relevant medical knowledge
            4. Triage Agent performs assessment using context + RAG
            5. Physician Matching Agent finds optimal doctors
            6. Scheduling Agent coordinates appointments
            7. Workflow Coordinator manages entire care journey
            """
            
            st.text(integration_flow)
            
            st.write("**Benefits of Integration:**")
            st.write("• **Accuracy**: Context + Medical Knowledge = Better Decisions")
            st.write("• **Efficiency**: Automated Agents = Faster Processing")
            st.write("• **Personalization**: Patient Context = Tailored Care")
            st.write("• **Safety**: Multiple Validation Layers = Reduced Errors")
            
            if st.button("🔄 Show Complete Integration"):
                st.success("✅ All systems integrated and operational")
                st.write("**Integration Status:**")
                st.write("🔍 RAG System: Connected to Qdrant Vector DB")
                st.write("🧠 Context Engine: Processing patient data")
                st.write("🤖 AI Agents: Coordinating patient journey")
                st.write("💾 Data Flow: Context → RAG → Agents → Results")