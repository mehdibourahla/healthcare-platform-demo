from typing import Dict
import uuid
import datetime
from models import Patient, TriageResult, UrgencyLevel

class WorkflowCoordinatorAgent:
    async def create_care_workflow(self, patient: Patient, triage_result: TriageResult, scheduling_result: Dict) -> Dict:
        """Create comprehensive care workflow"""
        print("   📋 Creating patient care workflow...")
        
        # Pre-appointment workflow
        pre_appointment = await self._create_pre_appointment_workflow(patient, triage_result, scheduling_result)
        print(f"   📝 Pre-appointment: {len(pre_appointment['tasks'])} tasks")
        
        # Appointment workflow
        appointment_workflow = await self._create_appointment_workflow(triage_result)
        print(f"   🏥 Appointment: {len(appointment_workflow['steps'])} steps")
        
        # Post-appointment workflow
        post_appointment = await self._create_post_appointment_workflow(triage_result)
        print(f"   📋 Post-appointment: {len(post_appointment['tasks'])} tasks")
        
        # Follow-up workflow
        follow_up = await self._create_follow_up_workflow(triage_result)
        print(f"   🔄 Follow-up: {len(follow_up['milestones'])} milestones")
        
        workflow_plan = {
            "workflow_id": str(uuid.uuid4())[:8],
            "patient_id": patient.patient_id,
            "created_at": datetime.datetime.now().isoformat(),
            "status": "active",
            "phases": {
                "pre_appointment": pre_appointment,
                "appointment": appointment_workflow, 
                "post_appointment": post_appointment,
                "follow_up": follow_up
            }
        }
        
        print(f"   ✅ Care workflow created: {workflow_plan['workflow_id']}")
        
        return workflow_plan
    
    async def _create_pre_appointment_workflow(self, patient: Patient, triage_result: TriageResult, scheduling_result: Dict) -> Dict:
        """Create pre-appointment workflow"""
        tasks = []
        
        # Standard pre-appointment tasks
        tasks.extend([
            {
                "task": "Send appointment confirmation",
                "status": "completed",
                "due_date": datetime.datetime.now().isoformat()
            },
            {
                "task": "Update patient portal",
                "status": "completed", 
                "due_date": datetime.datetime.now().isoformat()
            },
            {
                "task": "Send pre-appointment instructions",
                "status": "pending",
                "due_date": (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat()
            }
        ])
        
        # Risk-based tasks
        if triage_result.urgency_level in [UrgencyLevel.URGENT, UrgencyLevel.CRITICAL]:
            tasks.append({
                "task": "Contact patient to confirm appointment understanding",
                "status": "pending",
                "due_date": (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat()
            })
        
        # Specialty-specific preparations
        if triage_result.recommended_specialty == "cardiology":
            tasks.append({
                "task": "Order pre-visit EKG if indicated",
                "status": "pending",
                "due_date": (scheduling_result["appointment_time"] - datetime.timedelta(days=1)).isoformat()
            })
        
        return {
            "phase": "pre_appointment",
            "tasks": tasks,
            "completion_status": f"{len([t for t in tasks if t['status'] == 'completed'])}/{len(tasks)}"
        }
    
    async def _create_appointment_workflow(self, triage_result: TriageResult) -> Dict:
        """Create appointment day workflow"""
        steps = [
            {"step": "Patient check-in", "duration": "5 min", "responsible": "reception"},
            {"step": "Vital signs collection", "duration": "10 min", "responsible": "nurse"},
            {"step": "Medical history review", "duration": "5 min", "responsible": "nurse"},
            {"step": "Physician consultation", "duration": "20-30 min", "responsible": "physician"},
            {"step": "Treatment plan discussion", "duration": "10 min", "responsible": "physician"},
            {"step": "Schedule follow-up if needed", "duration": "5 min", "responsible": "reception"}
        ]
        
        # Urgency-based modifications
        if triage_result.urgency_level == UrgencyLevel.URGENT:
            steps.insert(2, {
                "step": "Rapid assessment protocol", 
                "duration": "10 min", 
                "responsible": "nurse"
            })
        
        return {
            "phase": "appointment",
            "steps": steps,
            "total_estimated_duration": f"{sum(int(s['duration'].split()[0].split('-')[0]) for s in steps)} minutes"
        }
    
    async def _create_post_appointment_workflow(self, triage_result: TriageResult) -> Dict:
        """Create post-appointment workflow"""
        tasks = [
            {
                "task": "Upload visit notes to EHR",
                "responsible": "physician",
                "due": "Within 24 hours"
            },
            {
                "task": "Send visit summary to patient",
                "responsible": "system",
                "due": "Within 2 hours"
            },
            {
                "task": "Process any lab/imaging orders",
                "responsible": "lab_coordinator", 
                "due": "Same day"
            }
        ]
        
        # Specialty-specific post-appointment tasks
        if triage_result.recommended_specialty == "cardiology":
            tasks.append({
                "task": "Review EKG results with patient",
                "responsible": "physician",
                "due": "Within 48 hours"
            })
        
        return {
            "phase": "post_appointment",
            "tasks": tasks
        }
    
    async def _create_follow_up_workflow(self, triage_result: TriageResult) -> Dict:
        """Create follow-up care workflow"""
        milestones = []
        
        # Standard follow-up based on urgency
        if triage_result.urgency_level in [UrgencyLevel.URGENT, UrgencyLevel.SEMI_URGENT]:
            milestones.extend([
                {
                    "milestone": "24-hour check-in call",
                    "due_date": (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(),
                    "responsible": "nurse"
                },
                {
                    "milestone": "1-week follow-up appointment",
                    "due_date": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat(),
                    "responsible": "scheduler"
                }
            ])
        
        # Standard follow-up
        milestones.append({
            "milestone": "Treatment response evaluation",
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=14)).isoformat(),
            "responsible": "physician"
        })
        
        return {
            "phase": "follow_up",
            "milestones": milestones
        }