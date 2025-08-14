import os

# Environment Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "your-cluster-url.qdrant.tech")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Model Configuration
EMBEDDINGS_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
VECTOR_SIZE = 1536

# Medical Configuration
MEDICAL_ACCURACY_THRESHOLD = 0.7
HUMAN_REVIEW_THRESHOLD = 0.8
SAFETY_THRESHOLD = 0.6

# Demo Configuration
DEMO_PATIENT_DATA = {
    "name": "Robert Martinez",
    "age": 52,
    "gender": "Male",
    "location": "Boston, MA",
    "phone": "+1 (555) 234-5678",
    "email": "robert.martinez@email.com",
    "insurance": "Blue Cross",
    "emergency_contact": "Maria Martinez - (555) 876-5432",
    "medical_history": ["Hypertension", "Diabetes"],
    "current_medications": [
        "Lisinopril 10mg daily (for blood pressure)",
        "Metformin 500mg twice daily (for diabetes)",
        "Atorvastatin 20mg daily (for cholesterol)",
        "Aspirin 81mg daily (cardio protection)"
    ],
    "allergies": ["Penicillin"],
    "family_history": ["Heart Disease", "Diabetes"],
    "lifestyle_factors": {
        "smoking": "Former",
        "alcohol": "Occasional",
        "exercise": "Weekly",
        "diet": "Standard",
        "sleep_hours": 6,
        "stress_level": 7
    }
}

DEMO_SYMPTOMS_DATA = {
    "primary_complaint": """I've been experiencing chest discomfort and shortness of breath, especially when walking upstairs or doing physical activity. The chest pain feels like pressure or tightness, and sometimes radiates to my left arm. This has been happening more frequently over the past week, and I'm concerned given my family history of heart disease.""",
    "symptoms": ["Chest pain", "Shortness of breath", "Fatigue"],
    "duration": "1-4 weeks",
    "severity": 6,
    "associated_symptoms": ["Sweating", "Palpitations"],
    "aggravating_factors": ["Movement", "Stress"],
    "relieving_factors": ["Rest"],
    "previous_episodes": True
}

# Medical Knowledge Base
MEDICAL_GUIDELINES = [
    {
        "id": "chest_pain_1",
        "title": "Chest Pain Assessment Protocol",
        "content": "Acute chest pain requires immediate evaluation for cardiovascular causes. Red flags include radiation to left arm, jaw pain, shortness of breath, diaphoresis. Consider STEMI, unstable angina, aortic dissection.",
        "specialty": "cardiology",
        "urgency": "high"
    },
    {
        "id": "headache_1", 
        "title": "Headache Triage Guidelines",
        "content": "Severe sudden-onset headache (thunderclap) warrants immediate imaging for subarachnoid hemorrhage. Progressive headaches with neurological symptoms require urgent evaluation.",
        "specialty": "neurology",
        "urgency": "medium"
    },
    {
        "id": "abdominal_1",
        "title": "Acute Abdominal Pain Protocol", 
        "content": "Right lower quadrant pain with fever and elevated WBC suggests appendicitis. McBurney's point tenderness is classic. Requires surgical consultation.",
        "specialty": "general_surgery",
        "urgency": "high"
    },
    {
        "id": "dermatology_1",
        "title": "Skin Lesion Assessment",
        "content": "ABCDE criteria for melanoma: Asymmetry, Border irregularity, Color variation, Diameter >6mm, Evolving. Any concerning lesions require dermatology referral.",
        "specialty": "dermatology", 
        "urgency": "medium"
    },
    {
        "id": "pediatric_1",
        "title": "Pediatric Fever Guidelines",
        "content": "Fever in infants <3 months requires immediate evaluation. High fever with petechial rash suggests meningococcemia. Always consider bacterial meningitis.",
        "specialty": "pediatrics",
        "urgency": "high"
    }
]

# Physician Database
PHYSICIANS_DATABASE = [
    {
        "id": "card_001",
        "name": "Sarah Johnson",
        "specialty": "Cardiology", 
        "location": "New York, NY",
        "availability": "Mon-Fri 9AM-5PM",
        "rating": 4.8,
        "accepts_insurance": ["Aetna", "Blue Cross", "Cigna", "UnitedHealth"]
    },
    {
        "id": "neuro_001",
        "name": "Michael Chen",
        "specialty": "Neurology",
        "location": "Boston, MA", 
        "availability": "Mon-Wed-Fri 8AM-4PM",
        "rating": 4.9,
        "accepts_insurance": ["Blue Cross", "Cigna", "Medicare"]
    },
    {
        "id": "gastro_001",
        "name": "Emily Rodriguez",
        "specialty": "Gastroenterology",
        "location": "Chicago, IL",
        "availability": "Tue-Thu 10AM-6PM",
        "rating": 4.7,
        "accepts_insurance": ["Aetna", "UnitedHealth", "Humana"]
    },
    {
        "id": "derm_001", 
        "name": "David Kim",
        "specialty": "Dermatology",
        "location": "Los Angeles, CA",
        "availability": "Mon-Fri 9AM-3PM",
        "rating": 4.6,
        "accepts_insurance": ["Blue Cross", "Aetna", "Kaiser"]
    },
    {
        "id": "ortho_001",
        "name": "Jessica Brown",
        "specialty": "Orthopedics",
        "location": "Houston, TX",
        "availability": "Mon-Thu 8AM-5PM",
        "rating": 4.8,
        "accepts_insurance": ["UnitedHealth", "Cigna", "Blue Cross"]
    },
    {
        "id": "general_001",
        "name": "Robert Wilson", 
        "specialty": "General Medicine",
        "location": "Miami, FL",
        "availability": "Mon-Fri 8AM-6PM",
        "rating": 4.5,
        "accepts_insurance": ["Aetna", "Blue Cross", "Medicaid"]
    }
]

# Specialty Keywords for Symptom Matching
SPECIALTY_KEYWORDS = {
    "cardiology": ["chest pain", "heart", "palpitations", "shortness of breath"],
    "neurology": ["headache", "dizziness", "numbness", "seizure", "stroke"],
    "gastroenterology": ["abdominal pain", "nausea", "vomiting", "diarrhea"],
    "dermatology": ["rash", "skin", "itching", "lesion"],
    "orthopedics": ["joint pain", "back pain", "fracture", "injury"],
    "pulmonology": ["cough", "breathing", "chest", "asthma"],
    "endocrinology": ["diabetes", "thyroid", "hormone"],
    "psychiatry": ["anxiety", "depression", "mood", "mental health"]
}

# Location Coordinates for Distance Calculation
LOCATION_COORDS = {
    "New York": (40.7128, -74.0060),
    "Boston": (42.3601, -71.0589),
    "Chicago": (41.8781, -87.6298),
    "Los Angeles": (34.0522, -118.2437),
    "Houston": (29.7604, -95.3698),
    "Miami": (25.7617, -80.1918)
}

# UI Configuration
STREAMLIT_CONFIG = {
    "page_title": "Healthcare Platform Demo",
    "page_icon": "🏥",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}