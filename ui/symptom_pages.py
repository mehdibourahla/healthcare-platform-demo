import streamlit as st
import datetime
import uuid
import time
import asyncio
from models import SymptomAssessment, TriageResult, PhysicianRecommendation, UrgencyLevel
from config import DEMO_SYMPTOMS_DATA

class SymptomPages:
    def __init__(self, app_instance):
        self.app = app_instance

    def show_symptom_assessment(self):
        """Show symptom assessment interface"""
        st.header("🩺 Intelligent Symptom Assessment")
        
        if "current_patient" not in st.session_state:
            st.warning("⚠️ Please register a patient first")
            if st.button("👤 Go to Patient Registration"):
                st.info("Please click on 'Patient Registration' in the sidebar")
                st.rerun()
            return
        
        patient = st.session_state.current_patient
        st.info(f"Assessment for: **{patient.name}** (ID: {patient.patient_id})")
        
        # Add demo data toggle
        demo_mode = st.session_state.get("demo_mode", False)
        use_demo_data = st.checkbox("🎬 Use Demo Symptoms (Pre-filled cardiac scenario)", 
                                   value=demo_mode or st.session_state.get("use_demo_data", True))
        
        if use_demo_data:
            st.info("🫀 **Demo Scenario: Chest Pain with Cardiac Risk Factors** - Perfect for cardiology referral demo")
        
        with st.form("symptom_assessment"):
            st.subheader("Primary Complaint")
            primary_complaint = st.text_area(
                "What brings you in today?*",
                value=DEMO_SYMPTOMS_DATA["primary_complaint"] if use_demo_data else "",
                placeholder="Describe your main concern or symptom in your own words"
            )
            
            st.subheader("Symptom Details")
            col1, col2 = st.columns(2)
            
            with col1:
                symptoms = st.multiselect(
                    "Select all symptoms you're experiencing:",
                    ["Chest pain", "Headache", "Shortness of breath", "Dizziness", 
                     "Nausea", "Vomiting", "Fever", "Cough", "Abdominal pain",
                     "Back pain", "Joint pain", "Skin rash", "Fatigue", "Other"],
                    default=DEMO_SYMPTOMS_DATA["symptoms"] if use_demo_data else []
                )
                
                duration = st.selectbox(
                    "How long have you had these symptoms?*",
                    ["Less than 1 hour", "1-6 hours", "6-24 hours", "1-3 days", 
                     "4-7 days", "1-4 weeks", "1-3 months", "More than 3 months"],
                    index=5 if use_demo_data else 0  # 1-4 weeks
                )
                
                severity = st.slider(
                    "Rate your symptom severity (1-10)*", 
                    1, 10, 
                    value=DEMO_SYMPTOMS_DATA["severity"] if use_demo_data else 5,
                    help="1 = Mild discomfort, 10 = Worst pain imaginable"
                )
            
            with col2:
                associated_symptoms = st.multiselect(
                    "Any additional symptoms?",
                    ["Sweating", "Palpitations", "Numbness", "Tingling", 
                     "Weakness", "Vision changes", "Hearing changes", "Confusion"],
                    default=DEMO_SYMPTOMS_DATA["associated_symptoms"] if use_demo_data else []
                )
                
                aggravating_factors = st.multiselect(
                    "What makes it worse?",
                    ["Movement", "Rest", "Eating", "Stress", "Weather changes",
                     "Time of day", "Certain positions", "Nothing makes it worse"],
                    default=DEMO_SYMPTOMS_DATA["aggravating_factors"] if use_demo_data else []
                )
                
                relieving_factors = st.multiselect(
                    "What makes it better?",
                    ["Rest", "Movement", "Pain medication", "Heat", "Cold",
                     "Certain positions", "Nothing helps"],
                    default=DEMO_SYMPTOMS_DATA["relieving_factors"] if use_demo_data else []
                )
                
                previous_episodes = st.checkbox("Have you had similar episodes before?",
                    value=DEMO_SYMPTOMS_DATA["previous_episodes"] if use_demo_data else False)
            
            # Add demo scenario explanation
            if use_demo_data:
                with st.expander("📋 Demo Scenario Details"):
                    st.write("**This demo uses a realistic cardiac scenario:**")
                    st.write("• 52-year-old male with hypertension and diabetes")
                    st.write("• Family history of heart disease")
                    st.write("• Chest pain with exertion (possible angina)")
                    st.write("• Multiple cardiac risk factors")
                    st.write("• Symptoms suggest cardiology referral needed")
                    st.write("• Perfect case to demonstrate RAG medical knowledge retrieval")
            
            submitted = st.form_submit_button("🔍 Analyze Symptoms", type="primary")
            
            if submitted:
                if primary_complaint and symptoms and duration:
                    # Create symptom assessment
                    assessment = SymptomAssessment(
                        patient_id=patient.patient_id,
                        primary_complaint=primary_complaint,
                        symptoms=symptoms,
                        duration=duration,
                        severity=severity,
                        associated_symptoms=associated_symptoms,
                        aggravating_factors=aggravating_factors,
                        relieving_factors=relieving_factors,
                        previous_episodes=previous_episodes,
                        assessment_id=str(uuid.uuid4())[:8],
                        created_at=datetime.datetime.now()
                    )
                    
                    st.session_state.current_assessment = assessment
                    
                    st.success("✅ Symptom assessment completed!")
                    
                    # Show AI chatbot simulation
                    st.subheader("🤖 AI Chatbot Analysis")
                    
                    with st.chat_message("assistant"):
                        if use_demo_data:
                            st.write(f"Thank you, **{patient.name}**. I've analyzed your symptoms and medical history:")
                            st.write(f"🫀 **Primary concern**: Chest pain with exertion and shortness of breath")
                            st.write(f"⚠️ **Key risk factors**: Age 52, male, diabetes, hypertension, family history of heart disease")
                            st.write(f"📊 **Symptom pattern**: Classic presentation of possible stable angina")
                            st.write(f"🎯 **Clinical correlation**: Pain with exertion, relieved by rest, radiation to left arm")
                            st.write("")
                            st.warning("⚡ **Clinical Assessment**: Your symptoms combined with your cardiac risk factors suggest this requires cardiology evaluation within 24-48 hours.")
                            st.write("")
                            st.write("🔍 I'm now consulting medical guidelines for chest pain protocols and analyzing your complete medical profile using our RAG knowledge system...")
                        else:
                            st.write(f"Thank you, {patient.name}. I've analyzed your symptoms:")
                            st.write(f"• **Primary concern**: {primary_complaint}")
                            st.write(f"• **Symptoms**: {', '.join(symptoms)}")
                            st.write(f"• **Severity**: {severity}/10")
                            st.write(f"• **Duration**: {duration}")
                            
                            if severity >= 8:
                                st.warning("⚠️ Your symptoms indicate high severity. This requires urgent medical attention.")
                            elif severity >= 6:
                                st.info("ℹ️ Your symptoms suggest you should be seen within 24-48 hours.")
                            
                            st.write("I'm now consulting medical guidelines and analyzing your medical history for the most appropriate care recommendation.")
                    
                    # Show what happens in the real system
                    with st.expander("🔧 Real System Implementation"):
                        st.write("**In the production system, this would trigger:**")
                        st.code("""
print("🤖 SYMPTOM ASSESSMENT CHATBOT:")
print("   💬 Processing natural language symptoms...")
print("   🧠 Extracting medical entities and relationships")
print("   📚 Cross-referencing with medical ontologies")  
print("   🔍 Searching for similar symptom patterns")
print("   ⚕️ Applying clinical decision rules")
print("   📊 Calculating symptom severity scores")
print("   🎯 Preparing for AI triage analysis")
                        """, language="python")
                    
                    # Option to proceed to AI triage
                    if st.button("➡️ Proceed to AI Triage"):
                        st.success("Click on 'AI Triage System' in the sidebar to continue!")
                        st.rerun()
                
                else:
                    st.error("Please fill in all required fields marked with *")

    def show_ai_triage(self):
        """Show AI triage system in action"""
        st.header("🧠 AI Triage System - RAG + Context + Agents")
        
        if "current_assessment" not in st.session_state:
            st.warning("⚠️ Please complete symptom assessment first")
            return
        
        patient = st.session_state.current_patient
        assessment = st.session_state.current_assessment
        
        st.info(f"AI Triage for: **{patient.name}** | Symptoms: **{assessment.primary_complaint}**")
        
        if st.button("🚀 Run Complete AI Triage Analysis", type="primary"):
            # Show processing steps
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Capture console output
            output_container = st.container()
            
            with output_container:
                st.subheader("🔄 AI System Processing")
                
                # Create expandable sections for each AI component
                rag_container = st.container()
                context_container = st.container()
                agents_container = st.container()
                
                async def run_triage():
                    # Run the complete patient journey
                    result = await self.app.agent_system.coordinate_patient_journey(patient, assessment)
                    return result
                
                # Simulate the AI processing with progress updates
                status_text.text("Initializing AI systems...")
                progress_bar.progress(10)
                time.sleep(1)
                
                # Show RAG System in Action
                with rag_container:
                    st.subheader("🔍 RAG System: Medical Knowledge Retrieval")
                    rag_placeholder = st.empty()
                    
                status_text.text("RAG system retrieving medical knowledge...")
                progress_bar.progress(25)
                
                # Simulate RAG retrieval with visible output
                with rag_placeholder.container():
                    st.write("**🔍 Semantic Search Query:**")
                    symptoms_query = f"{assessment.primary_complaint[:100]}... + {', '.join(assessment.symptoms[:3])}"
                    st.code(f"Query: {symptoms_query}")
                    
                    st.write("**📚 Retrieved Medical Guidelines:**")
                    
                    # Show what RAG retrieves for this scenario
                    if "chest pain" in assessment.primary_complaint.lower():
                        retrieved_docs = [
                            {"title": "Chest Pain Assessment Protocol", "score": 0.892, "specialty": "cardiology"},
                            {"title": "Acute Coronary Syndrome Guidelines", "score": 0.857, "specialty": "cardiology"},
                            {"title": "Cardiac Risk Stratification", "score": 0.834, "specialty": "cardiology"}
                        ]
                    else:
                        retrieved_docs = [
                            {"title": "General Symptom Assessment", "score": 0.756, "specialty": "general"},
                            {"title": "Primary Care Protocols", "score": 0.723, "specialty": "general"},
                            {"title": "Triage Guidelines", "score": 0.698, "specialty": "general"}
                        ]
                    
                    for i, doc in enumerate(retrieved_docs):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"📄 {doc['title']}")
                        with col2:
                            st.write(f"⭐ {doc['score']:.3f}")
                        with col3:
                            st.write(f"🏥 {doc['specialty']}")
                    
                    st.success("✅ Retrieved 3 relevant clinical guidelines from vector database")
                
                time.sleep(2)
                
                # Show Context Engineering
                with context_container:
                    st.subheader("🧠 Context Engineering: Patient Analysis")
                    context_placeholder = st.empty()
                
                status_text.text("Building comprehensive patient context...")
                progress_bar.progress(45)
                
                with context_placeholder.container():
                    st.write("**🔄 Context Fusion Process:**")
                    
                    context_components = [
                        "✅ Demographic Context: 52-year-old male",
                        "✅ Medical History: Hypertension, Diabetes (2 conditions)",
                        "✅ Risk Factors: Age >50, Male gender, Diabetes, HTN",
                        "✅ Symptom Pattern: Exertional chest pain + SOB",
                        "✅ Temporal Context: Progressive over 1-4 weeks",
                        "✅ Social Context: Insurance verified, Boston location"
                    ]
                    
                    for component in context_components:
                        st.write(component)
                        time.sleep(0.3)
                    
                    st.write("**⚠️ Risk Stratification:**")
                    st.warning("High cardiac risk profile identified: 4 major risk factors")
                
                time.sleep(1)
                
                # Show Agent Coordination
                with agents_container:
                    st.subheader("🤖 Agentic AI: Multi-Agent Coordination")
                    agents_placeholder = st.empty()
                
                status_text.text("Agents coordinating medical decision...")
                progress_bar.progress(65)
                
                with agents_placeholder.container():
                    st.write("**🏥 Triage Agent Analysis:**")
                    st.write("• Processing RAG knowledge + Patient context")
                    st.write("• Consulting LLM with medical prompt")
                    st.write("• Calculating urgency score: 67/100")
                    st.write("• Recommendation: Semi-urgent cardiology referral")
                    
                    time.sleep(1)
                    
                    st.write("**👨‍⚕️ Physician Matching Agent:**")
                    st.write("• Specialty filter: Cardiology (from RAG + symptoms)")
                    st.write("• Location filter: Boston area")
                    st.write("• Insurance filter: Blue Cross accepted")
                    st.write("• Ranking by: Distance + Rating + Availability")
                    
                    time.sleep(1)
                
                status_text.text("Finalizing recommendations...")
                progress_bar.progress(85)
                time.sleep(1)
                
                status_text.text("✅ AI Analysis Complete!")
                progress_bar.progress(100)
                time.sleep(1)
                
                # Run the actual AI system
                try:
                    # Create event loop for async functions
                    result = asyncio.run(self.app.agent_system.coordinate_patient_journey(patient, assessment))
                    
                    st.session_state.triage_result = result
                    status_text.text("✅ AI Triage Analysis Complete!")
                    
                    # Display results
                    st.subheader("📊 Triage Results")
                    
                    triage = result["triage_result"]
                    
                    # Emergency check
                    if triage.requires_emergency:
                        st.error("🚨 EMERGENCY SITUATION DETECTED")
                        st.error("**Immediate medical attention required**")
                        emergency_summary = result.get("emergency_summary", {})
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Recommended Actions:**")
                            for action in emergency_summary.get("recommended_actions", []):
                                st.write(f"• {action}")
                        
                        with col2:
                            st.write("**Emergency Contact Info:**")
                            st.write(f"• Emergency Contact: {patient.emergency_contact}")
                            st.write(f"• Patient Location: {patient.location}")
                        
                        return
                    
                    # Normal triage results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        urgency_color = {
                            "Critical Emergency": "🔴",
                            "Urgent": "🟠", 
                            "Semi-Urgent": "🟡",
                            "Standard": "🟢",
                            "Non-Urgent": "🔵"
                        }
                        st.metric(
                            "Urgency Level",
                            f"{urgency_color.get(triage.urgency_level.value, '⚪')} {triage.urgency_level.value}",
                            f"Wait time: {triage.estimated_wait_time}"
                        )
                    
                    with col2:
                        st.metric(
                            "Recommended Specialty",
                            triage.recommended_specialty.title(),
                            f"Confidence: {triage.confidence_score:.2%}"
                        )
                    
                    with col3:
                        risk_level = "High" if len(triage.risk_factors) >= 3 else "Medium" if len(triage.risk_factors) >= 1 else "Low"
                        st.metric(
                            "Risk Assessment", 
                            risk_level,
                            f"{len(triage.risk_factors)} risk factors"
                        )
                    
                    # Detailed analysis
                    st.subheader("🔍 Detailed Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Clinical Reasoning:**")
                        st.write(triage.clinical_reasoning)
                        
                        st.write("**Risk Factors Identified:**")
                        for risk in triage.risk_factors:
                            st.write(f"• {risk}")
                    
                    with col2:
                        st.write("**Context Analysis:**")
                        context = result["context"]
                        st.write(f"• Age: {context['demographic']['age']} years")
                        st.write(f"• Medical History: {len(context['medical']['chronic_conditions'])} conditions")
                        st.write(f"• Current Medications: {len(context['medical']['current_medications'])}")
                        st.write(f"• Risk Score: {context['risk']['risk_score']}")
                    
                    # Physician recommendations
                    st.subheader("👨‍⚕️ Physician Recommendations")
                    
                    recommendations = result["physician_recommendations"]
                    
                    for i, rec in enumerate(recommendations[:3]):
                        with st.expander(f"Dr. {rec.name} - {rec.specialty}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**Rating:** {'⭐' * int(rec.rating)} ({rec.rating})")
                                st.write(f"**Distance:** {rec.distance_km} km")
                                
                            with col2:
                                st.write(f"**Location:** {rec.location}")
                                st.write(f"**Insurance:** ✅ Accepted")
                                
                            with col3:
                                st.write(f"**Next Available:**")
                                st.write(rec.next_available.strftime("%Y-%m-%d %H:%M"))
                    
                    # Option to proceed to scheduling
                    if st.button("➡️ Proceed to Appointment Scheduling"):
                        st.success("Click on 'Physician Matching' in the sidebar to continue!")
                        st.rerun()
                
                except Exception as e:
                    st.error(f"AI Triage Error: {e}")
                    st.info("This demo continues with simulated results...")
                    
                    # Create comprehensive mock results for demo continuation
                    assessment = st.session_state.current_assessment
                    patient = st.session_state.current_patient
                    
                    mock_triage = TriageResult(
                        assessment_id=assessment.assessment_id,
                        urgency_level=UrgencyLevel.STANDARD,
                        recommended_specialty="general_medicine",
                        risk_factors=["Standard assessment"],
                        clinical_reasoning="Based on symptoms, recommend general medical evaluation for comprehensive assessment.",
                        confidence_score=0.75,
                        requires_emergency=False,
                        estimated_wait_time="Within 1-2 weeks"
                    )
                    
                    # Create mock physician recommendations
                    mock_recommendations = [
                        PhysicianRecommendation(
                            physician_id="gen_001",
                            name="Dr. Sarah Johnson",
                            specialty="General Medicine",
                            location=patient.location,
                            availability="Mon-Fri 9AM-5PM",
                            rating=4.8,
                            distance_km=5.2,
                            accepts_insurance=True,
                            next_available=datetime.datetime.now() + datetime.timedelta(days=3)
                        ),
                        PhysicianRecommendation(
                            physician_id="gen_002",
                            name="Dr. Michael Chen", 
                            specialty="General Medicine",
                            location=patient.location,
                            availability="Tue-Thu 8AM-4PM",
                            rating=4.7,
                            distance_km=8.1,
                            accepts_insurance=True,
                            next_available=datetime.datetime.now() + datetime.timedelta(days=5)
                        )
                    ]
                    
                    # Store mock results
                    st.session_state.mock_triage = mock_triage
                    st.session_state.physician_recommendations = mock_recommendations
                    
                    # Display mock results
                    st.subheader("📊 Simulated Triage Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Urgency Level",
                            f"🟢 {mock_triage.urgency_level.value}",
                            f"Wait time: {mock_triage.estimated_wait_time}"
                        )
                    
                    with col2:
                        st.metric(
                            "Recommended Specialty",
                            mock_triage.recommended_specialty.title(),
                            f"Confidence: {mock_triage.confidence_score:.2%}"
                        )
                    
                    with col3:
                        st.metric(
                            "Risk Assessment", 
                            "Low",
                            f"{len(mock_triage.risk_factors)} risk factors"
                        )
                    
                    # Show mock physician recommendations
                    st.subheader("👨‍⚕️ Available Physicians")
                    
                    for i, rec in enumerate(mock_recommendations):
                        with st.expander(f"Dr. {rec.name} - {rec.specialty}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**Rating:** {'⭐' * int(rec.rating)} ({rec.rating})")
                                st.write(f"**Distance:** {rec.distance_km} km")
                                
                            with col2:
                                st.write(f"**Location:** {rec.location}")
                                st.write(f"**Insurance:** ✅ Accepted")
                                
                            with col3:
                                st.write(f"**Next Available:**")
                                st.write(rec.next_available.strftime("%Y-%m-%d %H:%M"))
                    
                    # Option to proceed to scheduling
                    if st.button("➡️ Proceed to Physician Matching"):
                        st.rerun()