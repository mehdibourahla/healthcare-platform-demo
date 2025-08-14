from typing import Dict, List
import uuid
from models import Patient, TriageResult, PhysicianRecommendation, UrgencyLevel

class AppointmentSchedulingAgent:
    async def schedule_appointment(self, patient: Patient, triage_result: TriageResult, physician_recommendations: List[PhysicianRecommendation]) -> Dict:
        """Schedule appointment with optimal physician"""
        print("   📋 Evaluating scheduling options...")
        
        if not physician_recommendations:
            print("   ❌ No physicians available")
            return {"status": "failed", "reason": "No physicians available"}
        
        # Select best physician (already sorted)
        selected_physician = physician_recommendations[0]
        
        print(f"   👨‍⚕️ Selected: Dr. {selected_physician.name}")
        print(f"   📅 Appointment time: {selected_physician.next_available.strftime('%Y-%m-%d %H:%M')}")
        print(f"   📍 Location: {selected_physician.location}")
        
        # Generate appointment details
        appointment_id = str(uuid.uuid4())[:8]
        
        # Pre-appointment preparation
        prep_tasks = self._generate_prep_tasks(triage_result, patient)
        print(f"   📝 Pre-appointment tasks: {len(prep_tasks)} items")
        
        # Send notifications (simulated)
        print("   📧 Sending confirmation email...")
        print("   📱 Sending SMS reminder...")
        print("   📋 Updating patient portal...")
        
        scheduling_result = {
            "appointment_id": appointment_id,
            "status": "confirmed", 
            "physician": selected_physician,
            "appointment_time": selected_physician.next_available,
            "location": selected_physician.location,
            "estimated_duration": "30 minutes",
            "prep_tasks": prep_tasks,
            "confirmation_sent": True,
            "calendar_updated": True
        }
        
        print(f"   ✅ Appointment {appointment_id} confirmed")
        
        return scheduling_result
    
    def _generate_prep_tasks(self, triage_result: TriageResult, patient: Patient) -> List[str]:
        """Generate pre-appointment preparation tasks"""
        tasks = [
            "Bring photo ID and insurance card",
            "Arrive 15 minutes early for check-in", 
            "Bring current medication list",
            "Prepare list of questions for doctor"
        ]
        
        # Specialty-specific tasks
        specialty_tasks = {
            "cardiology": [
                "Avoid caffeine 4 hours before appointment",
                "Bring any previous EKG or cardiac test results"
            ],
            "dermatology": [
                "Avoid makeup on affected areas",
                "Bring photos of skin changes over time"
            ],
            "gastroenterology": [
                "Fast for 8 hours if blood work needed",
                "Keep symptom diary until appointment"
            ]
        }
        
        specialty = triage_result.recommended_specialty.lower()
        if specialty in specialty_tasks:
            tasks.extend(specialty_tasks[specialty])
        
        # Urgency-specific tasks
        if triage_result.urgency_level in [UrgencyLevel.URGENT, UrgencyLevel.CRITICAL]:
            tasks.extend([
                "Arrange transportation (do not drive if feeling unwell)",
                "Notify emergency contact of appointment"
            ])
        
        return tasks