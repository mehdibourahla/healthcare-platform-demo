from typing import Dict, List
import datetime
from models import Patient, SymptomAssessment

class MedicalContextEngineer:
    def __init__(self):
        self.patient_graphs = {}
        
    async def build_comprehensive_context(self, patient: Patient, assessment: SymptomAssessment) -> Dict:
        """Build comprehensive medical context for the patient"""
        print(f"\n🧠 CONTEXT ENGINEERING:")
        print(f"   Building context for patient: {patient.name}")
        
        # Patient demographic context
        demographic_context = {
            "age": patient.age,
            "gender": patient.gender,
            "location": patient.location
        }
        print(f"   📊 Demographic context: {demographic_context}")
        
        # Medical history context
        medical_context = {
            "chronic_conditions": patient.medical_history,
            "current_medications": patient.current_medications,
            "allergies": patient.allergies,
            "family_history": patient.family_history
        }
        print(f"   🏥 Medical history context: {len(patient.medical_history)} conditions")
        
        # Current symptom context
        symptom_context = {
            "primary_complaint": assessment.primary_complaint,
            "symptoms": assessment.symptoms,
            "severity": assessment.severity,
            "duration": assessment.duration,
            "associated_symptoms": assessment.associated_symptoms
        }
        print(f"   🩺 Symptom context: {len(assessment.symptoms)} symptoms, severity {assessment.severity}/10")
        
        # Risk stratification context
        risk_context = self._calculate_risk_factors(patient, assessment)
        print(f"   ⚠️ Risk factors identified: {len(risk_context['risk_factors'])}")
        
        # Temporal context (simulated)
        temporal_context = {
            "time_of_day": datetime.datetime.now().strftime("%H:%M"),
            "day_of_week": datetime.datetime.now().strftime("%A"),
            "season": self._get_season()
        }
        print(f"   ⏰ Temporal context: {temporal_context['time_of_day']} on {temporal_context['day_of_week']}")
        
        # Social determinants context
        social_context = {
            "insurance_status": patient.insurance,
            "location_access": self._assess_location_access(patient.location),
            "emergency_support": bool(patient.emergency_contact)
        }
        print(f"   🏘️ Social context: Insurance {patient.insurance}")
        
        comprehensive_context = {
            "demographic": demographic_context,
            "medical": medical_context, 
            "symptom": symptom_context,
            "risk": risk_context,
            "temporal": temporal_context,
            "social": social_context
        }
        
        # Context validation
        validation_result = self._validate_context_consistency(comprehensive_context)
        print(f"   ✅ Context validation: {validation_result['status']}")
        
        return comprehensive_context
    
    def _calculate_risk_factors(self, patient: Patient, assessment: SymptomAssessment) -> Dict:
        """Calculate patient-specific risk factors"""
        risk_factors = []
        
        # Age-based risks
        if patient.age > 65:
            risk_factors.append("Advanced age")
        elif patient.age < 2:
            risk_factors.append("Pediatric patient")
            
        # Medical history risks
        high_risk_conditions = ["diabetes", "heart disease", "hypertension", "cancer"]
        for condition in patient.medical_history:
            if any(risk in condition.lower() for risk in high_risk_conditions):
                risk_factors.append(f"History of {condition}")
        
        # Medication risks
        high_risk_meds = ["warfarin", "insulin", "chemotherapy"]
        for med in patient.current_medications:
            if any(risk in med.lower() for risk in high_risk_meds):
                risk_factors.append(f"High-risk medication: {med}")
        
        # Symptom-based risks
        if assessment.severity >= 8:
            risk_factors.append("High severity symptoms")
            
        red_flag_symptoms = ["chest pain", "severe headache", "difficulty breathing"]
        for symptom in assessment.symptoms:
            if any(flag in symptom.lower() for flag in red_flag_symptoms):
                risk_factors.append(f"Red flag symptom: {symptom}")
        
        return {
            "risk_factors": risk_factors,
            "risk_score": len(risk_factors),
            "high_risk": len(risk_factors) >= 3
        }
    
    def _get_season(self) -> str:
        """Determine current season for epidemiological context"""
        month = datetime.datetime.now().month
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"
    
    def _assess_location_access(self, location: str) -> Dict:
        """Assess healthcare access based on location"""
        # Simplified location access assessment
        urban_areas = ["New York", "Los Angeles", "Chicago", "Boston"]
        if any(city in location for city in urban_areas):
            return {"access_level": "High", "specialty_available": True}
        else:
            return {"access_level": "Medium", "specialty_available": False}
    
    def _validate_context_consistency(self, context: Dict) -> Dict:
        """Validate medical context for consistency"""
        issues = []
        
        # Check age-medication consistency
        if context["demographic"]["age"] < 18:
            adult_meds = ["warfarin", "metformin"]
            for med in context["medical"]["current_medications"]:
                if any(adult_med in med.lower() for adult_med in adult_meds):
                    issues.append(f"Pediatric patient on adult medication: {med}")
        
        # Check symptom-duration consistency
        if context["symptom"]["severity"] >= 9 and "months" in context["symptom"]["duration"].lower():
            issues.append("Severe symptoms persisting for months - needs review")
        
        return {
            "status": "Valid" if not issues else "Needs Review",
            "issues": issues,
            "consistency_score": max(0, 1.0 - len(issues) * 0.2)
        }