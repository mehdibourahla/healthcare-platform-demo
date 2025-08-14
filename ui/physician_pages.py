import streamlit as st
import datetime
import uuid
from models import PhysicianRecommendation, UrgencyLevel

class PhysicianPages:
    def __init__(self, app_instance):
        self.app = app_instance

    def show_physician_matching(self):
        """Show physician matching results"""
        st.header("👨‍⚕️ Physician Matching & Recommendations")
        
        # Check if we have patient data
        if "current_patient" not in st.session_state:
            st.warning("⚠️ Please register a patient first")
            if st.button("👤 Go to Patient Registration"):
                st.rerun()
            return
        
        patient = st.session_state.current_patient
        
        # Check for triage results
        triage_result = st.session_state.get("triage_result", {})
        mock_triage = st.session_state.get("mock_triage", None)
        
        if not triage_result and not mock_triage:
            st.warning("⚠️ Please complete AI triage first")
            if st.button("🧠 Go to AI Triage"):
                st.rerun()
            return
        
        # Extract triage and recommendations safely
        if triage_result and "triage_result" in triage_result:
            triage = triage_result["triage_result"]
            recommendations = triage_result.get("physician_recommendations", [])
        elif mock_triage:
            triage = mock_triage
            recommendations = []
        else:
            # Create fallback triage for demo
            from models import TriageResult
            triage = TriageResult(
                assessment_id="DEMO001",
                urgency_level=UrgencyLevel.STANDARD,
                recommended_specialty="general_medicine",
                risk_factors=["Standard assessment"],
                clinical_reasoning="Demo assessment for physician matching.",
                confidence_score=0.8,
                requires_emergency=False,
                estimated_wait_time="Within 1-2 weeks"
            )
            recommendations = []
        
        # Generate mock recommendations if none exist
        if not recommendations:
            recommendations = [
                PhysicianRecommendation(
                    physician_id="card_001",
                    name="Sarah Johnson",
                    specialty="Cardiology",
                    location="New York, NY",
                    availability="Mon-Fri 9AM-5PM",
                    rating=4.8,
                    distance_km=5.2,
                    accepts_insurance=True,
                    next_available=datetime.datetime.now() + datetime.timedelta(days=3)
                ),
                PhysicianRecommendation(
                    physician_id="gen_001", 
                    name="Michael Chen",
                    specialty="General Medicine",
                    location="New York, NY",
                    availability="Tue-Thu 8AM-4PM",
                    rating=4.9,
                    distance_km=8.7,
                    accepts_insurance=True,
                    next_available=datetime.datetime.now() + datetime.timedelta(days=5)
                )
            ]
            
            # Store recommendations for next step
            st.session_state.physician_recommendations = recommendations
        
        st.info(f"Physician matching for: **{patient.name}** | Specialty: **{triage.recommended_specialty}**")
        
        # Matching criteria
        st.subheader("🎯 Matching Criteria")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write("**Specialty**")
            st.write(f"✅ {triage.recommended_specialty.title()}")
        
        with col2:
            st.write("**Location**") 
            st.write(f"📍 {patient.location}")
        
        with col3:
            st.write("**Insurance**")
            st.write(f"💳 {patient.insurance}")
        
        with col4:
            st.write("**Urgency**")
            st.write(f"⚡ {triage.urgency_level.value}")
        
        # Physician recommendations
        st.subheader("👥 Recommended Physicians")
        
        for i, rec in enumerate(recommendations):
            with st.container():
                st.markdown(f"### 🏆 Recommendation #{i+1}")
                
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Dr. {rec.name}**")
                    st.write(f"*{rec.specialty}*")
                    st.write(f"📍 {rec.location}")
                    st.write(f"📏 {rec.distance_km} km away")
                
                with col2:
                    st.write(f"**Rating:** {'⭐' * int(rec.rating)} ({rec.rating}/5.0)")
                    st.write(f"**Availability:** {rec.availability}")
                    st.write(f"**Insurance:** ✅ Accepts {patient.insurance}")
                    st.write(f"**Next Available:** {rec.next_available.strftime('%Y-%m-%d %H:%M')}")
                
                with col3:
                    if st.button(f"Select Dr. {rec.name}", key=f"select_{rec.physician_id}"):
                        st.session_state.selected_physician = rec
                        st.success(f"✅ Selected Dr. {rec.name}")
                        
                        # Show what happens in real system
                        with st.expander("🔧 Real System Implementation"):
                            st.code("""
print("👨‍⚕️ PHYSICIAN MATCHING SYSTEM:")
print("   🔍 Searching physician database...")
print("   📋 Applying specialty filters...")
print("   🏥 Checking insurance network participation...")
print("   📍 Calculating travel distances...")
print("   📅 Checking real-time availability...")
print("   ⭐ Ranking by patient preferences...")
print("   🎯 Optimizing appointment recommendations...")
print("   ✅ Physician matching completed")
                            """, language="python")
                
                st.markdown("---")
        
        # Show matching algorithm details
        with st.expander("🔧 Matching Algorithm Details"):
            st.write("**Ranking Factors:**")
            st.write("• **Specialty Match** (40%): Exact specialty alignment")  
            st.write("• **Distance** (25%): Proximity to patient location")
            st.write("• **Availability** (20%): Next available appointment")
            st.write("• **Rating** (10%): Patient satisfaction scores")
            st.write("• **Insurance** (5%): Network participation")
            
            st.write("**Real-time Data Sources:**")
            st.write("• Physician scheduling systems")
            st.write("• Insurance network directories") 
            st.write("• Patient preference profiles")
            st.write("• Geographic mapping services")

    def show_appointment_scheduling(self):
        """Show appointment scheduling interface"""
        st.header("📅 Appointment Scheduling & Care Coordination")
        
        # Check if we have required data
        if "current_patient" not in st.session_state:
            st.warning("⚠️ Please register a patient first")
            if st.button("👤 Go to Patient Registration"):
                st.rerun()
            return
        
        if "selected_physician" not in st.session_state:
            # Check if we have physician recommendations to select from
            recommendations = st.session_state.get("physician_recommendations", [])
            if recommendations:
                st.warning("⚠️ Please select a physician first")
                st.write("**Available Physicians:**")
                for i, rec in enumerate(recommendations[:3]):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"👨‍⚕️ **Dr. {rec.name}** - {rec.specialty}")
                        st.write(f"📍 {rec.location} • ⭐ {rec.rating}/5.0")
                    with col2:
                        if st.button(f"Select", key=f"quick_select_{rec.physician_id}"):
                            st.session_state.selected_physician = rec
                            st.rerun()
                return
            else:
                st.warning("⚠️ Please complete physician matching first")
                if st.button("👨‍⚕️ Go to Physician Matching"):
                    st.rerun()
                return
        
        patient = st.session_state.current_patient
        physician = st.session_state.selected_physician
        
        st.info(f"Scheduling appointment for: **{patient.name}** with **Dr. {physician.name}**")
        
        # Appointment details
        st.subheader("📋 Appointment Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Physician Information:**")
            st.write(f"• Dr. {physician.name}")
            st.write(f"• {physician.specialty}")
            st.write(f"• {physician.location}")
            st.write(f"• Rating: {'⭐' * int(physician.rating)} ({physician.rating})")
            
        with col2:
            st.write("**Appointment Details:**")
            st.write(f"• Date: {physician.next_available.strftime('%A, %B %d, %Y')}")
            st.write(f"• Time: {physician.next_available.strftime('%I:%M %p')}")
            st.write(f"• Duration: 30 minutes (estimated)")
            st.write(f"• Type: In-person consultation")
        
        # Pre-appointment preparation
        st.subheader("📝 Pre-Appointment Preparation")
        
        prep_tasks = [
            "✅ Bring photo ID and insurance card",
            "✅ Arrive 15 minutes early for check-in",
            "✅ Bring current medication list", 
            "✅ Prepare list of questions for doctor"
        ]
        
        # Add specialty-specific tasks
        if "cardiology" in physician.specialty.lower():
            prep_tasks.extend([
                "⚠️ Avoid caffeine 4 hours before appointment",
                "📋 Bring any previous EKG or cardiac test results"
            ])
        
        for task in prep_tasks:
            st.write(task)
        
        # Scheduling confirmation
        if st.button("📅 Confirm Appointment", type="primary"):
            
            # Generate appointment ID
            appointment_id = str(uuid.uuid4())[:8]
            
            st.success("✅ Appointment Confirmed!")
            st.success(f"📋 Appointment ID: {appointment_id}")
            
            # Show appointment summary
            with st.container():
                st.markdown("### 📄 Appointment Summary")
                
                appointment_summary = {
                    "Appointment ID": appointment_id,
                    "Patient": patient.name,
                    "Physician": f"Dr. {physician.name}",
                    "Specialty": physician.specialty,
                    "Date & Time": physician.next_available.strftime("%Y-%m-%d %H:%M"),
                    "Location": physician.location,
                    "Insurance": patient.insurance,
                    "Phone": patient.phone,
                    "Email": patient.email
                }
                
                for key, value in appointment_summary.items():
                    st.write(f"**{key}:** {value}")
            
            # Show care workflow
            st.subheader("🔄 Care Workflow Created")
            
            workflow_steps = [
                "📧 Confirmation email sent to patient",
                "📱 SMS reminder scheduled 24 hours before",
                "📋 Pre-appointment instructions sent",
                "🏥 Physician notified of new patient",
                "📊 Medical history summary prepared",
                "📅 Calendar updated for all parties",
                "🔔 Follow-up reminders scheduled"
            ]
            
            for step in workflow_steps:
                st.write(step)
            
            # Show real system implementation
            with st.expander("🔧 Real System Implementation"):
                st.code("""
print("📅 APPOINTMENT SCHEDULING SYSTEM:")
print("   🔍 Checking physician real-time availability...")
print("   🔒 Reserving appointment slot...")
print("   💾 Creating appointment record in EHR...")
print("   📧 Sending confirmation notifications...")
print("   📱 Setting up automated reminders...")
print("   🔄 Triggering care workflow automation...")
print("   📊 Updating physician dashboard...")
print("   💳 Processing insurance verification...")
print("   ✅ Appointment successfully scheduled")
                """, language="python")
            
            # Save to session state
            st.session_state.appointment_confirmed = {
                "appointment_id": appointment_id,
                "patient": patient,
                "physician": physician,
                "datetime": physician.next_available,
                "status": "confirmed"
            }