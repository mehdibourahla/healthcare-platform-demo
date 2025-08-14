from dataclasses import dataclass
from typing import Dict, List
import datetime
from .enums import UrgencyLevel

@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    location: str
    phone: str
    email: str
    insurance: str
    emergency_contact: str
    medical_history: List[str]
    current_medications: List[str]
    allergies: List[str]
    family_history: List[str]
    lifestyle_factors: Dict[str, str]
    created_at: datetime.datetime

@dataclass
class SymptomAssessment:
    patient_id: str
    primary_complaint: str
    symptoms: List[str]
    duration: str
    severity: int
    associated_symptoms: List[str]
    aggravating_factors: List[str]
    relieving_factors: List[str]
    previous_episodes: bool
    assessment_id: str
    created_at: datetime.datetime

@dataclass
class TriageResult:
    assessment_id: str
    urgency_level: UrgencyLevel
    recommended_specialty: str
    risk_factors: List[str]
    clinical_reasoning: str
    confidence_score: float
    requires_emergency: bool
    estimated_wait_time: str

@dataclass
class PhysicianRecommendation:
    physician_id: str
    name: str
    specialty: str
    location: str
    availability: str
    rating: float
    distance_km: float
    accepts_insurance: bool
    next_available: datetime.datetime