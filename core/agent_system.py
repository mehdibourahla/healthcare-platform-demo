from typing import Dict
import datetime
from models import Patient, SymptomAssessment, UrgencyLevel
from .rag_system import MedicalKnowledgeRAG
from .context_engine import MedicalContextEngineer
from agents import (
    TriageAgent,
    PhysicianMatchingAgent, 
    AppointmentSchedulingAgent,
    WorkflowCoordinatorAgent
)

class MedicalAgentSystem:
    def __init__(self, rag_system: MedicalKnowledgeRAG, context_engineer: MedicalContextEngineer):
        self.rag_system = rag_system
        self.context_engineer = context_engineer
        self.agents = {
            "triage": TriageAgent(),
            "physician_matcher": PhysicianMatchingAgent(),
            "scheduler": AppointmentSchedulingAgent(),
            "workflow_coordinator": WorkflowCoordinatorAgent()
        }
    
    async def coordinate_patient_journey(self, patient: Patient, assessment: SymptomAssessment) -> Dict:
        """Coordinate the complete patient journey using multiple agents"""
        print(f"\n🤖 AGENTIC AI COORDINATION:")
        print(f"   Starting patient journey for: {patient.name}")
        
        # Build comprehensive context
        context = await self.context_engineer.build_comprehensive_context(patient, assessment)
        
        # Agent 1: Triage Agent
        print(f"\n   🏥 AGENT 1: Medical Triage")
        triage_result = await self.agents["triage"].perform_triage(
            assessment, context, self.rag_system
        )
        
        # Safety check for emergency situations
        if triage_result.requires_emergency:
            print("   🚨 EMERGENCY ESCALATION TRIGGERED")
            return await self._handle_emergency_escalation(patient, assessment, triage_result)
        
        # Agent 2: Physician Matching
        print(f"\n   👨‍⚕️ AGENT 2: Physician Matching")
        physician_recommendations = await self.agents["physician_matcher"].match_physicians(
            triage_result, patient, context
        )
        
        # Agent 3: Appointment Scheduling
        print(f"\n   📅 AGENT 3: Appointment Scheduling")
        scheduling_result = await self.agents["scheduler"].schedule_appointment(
            patient, triage_result, physician_recommendations
        )
        
        # Agent 4: Workflow Coordination
        print(f"\n   🔄 AGENT 4: Workflow Coordination")
        workflow_plan = await self.agents["workflow_coordinator"].create_care_workflow(
            patient, triage_result, scheduling_result
        )
        
        return {
            "patient": patient,
            "assessment": assessment,
            "context": context,
            "triage_result": triage_result,
            "physician_recommendations": physician_recommendations,
            "scheduling_result": scheduling_result,
            "workflow_plan": workflow_plan,
            "journey_status": "Completed"
        }
    
    async def _handle_emergency_escalation(self, patient: Patient, assessment: SymptomAssessment, triage_result) -> Dict:
        """Handle emergency situations with immediate escalation"""
        print("   🚨 EMERGENCY PROTOCOL ACTIVATED")
        print("   📞 Contacting emergency services...")
        print("   🏥 Notifying nearest emergency department...")
        print("   📋 Preparing emergency medical summary...")
        
        emergency_summary = {
            "patient_id": patient.patient_id,
            "emergency_level": "CRITICAL",
            "primary_symptoms": assessment.symptoms,
            "medical_history": patient.medical_history,
            "current_medications": patient.current_medications,
            "allergies": patient.allergies,
            "emergency_contact": patient.emergency_contact,
            "estimated_arrival": "Immediate transport recommended",
            "recommended_actions": [
                "Call 911 immediately",
                "Do not drive yourself",
                "Have someone stay with you",
                "Bring medication list and ID"
            ]
        }
        
        return {
            "patient": patient,
            "assessment": assessment,
            "triage_result": triage_result,
            "emergency_summary": emergency_summary,
            "journey_status": "Emergency Escalation"
        }