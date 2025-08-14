from typing import Dict, List
import datetime
from models import Patient, TriageResult, PhysicianRecommendation, UrgencyLevel
from config import PHYSICIANS_DATABASE, LOCATION_COORDS

class PhysicianMatchingAgent:
    def __init__(self):
        self.physicians_db = PHYSICIANS_DATABASE
    
    async def match_physicians(self, triage_result: TriageResult, patient: Patient, context: Dict) -> List[PhysicianRecommendation]:
        """Match patient with appropriate physicians"""
        print("   🔍 Searching physician database...")
        print(f"   📋 Filtering by specialty: {triage_result.recommended_specialty}")
        print(f"   🏥 Patient location: {patient.location}")
        print(f"   💳 Insurance: {patient.insurance}")
        
        # Filter physicians by specialty
        specialty_matches = [
            p for p in self.physicians_db 
            if p["specialty"].lower() == triage_result.recommended_specialty.lower() or 
               triage_result.recommended_specialty.lower() in p["specialty"].lower()
        ]
        
        print(f"   ✅ Found {len(specialty_matches)} specialists")
        
        # Filter by insurance
        insurance_matches = [
            p for p in specialty_matches 
            if patient.insurance.lower() in [ins.lower() for ins in p["accepts_insurance"]]
        ]
        
        print(f"   ✅ {len(insurance_matches)} accept patient's insurance")
        
        # Calculate distance and availability
        recommendations = []
        for physician in insurance_matches[:5]:  # Top 5 matches
            distance = self._calculate_distance(patient.location, physician["location"])
            next_available = self._calculate_next_availability(physician, triage_result.urgency_level)
            
            recommendation = PhysicianRecommendation(
                physician_id=physician["id"],
                name=physician["name"],
                specialty=physician["specialty"],
                location=physician["location"],
                availability=physician["availability"],
                rating=physician["rating"],
                distance_km=distance,
                accepts_insurance=True,
                next_available=next_available
            )
            recommendations.append(recommendation)
            
            print(f"   👨‍⚕️ Match: Dr. {physician['name']} - {distance}km away, available {next_available.strftime('%Y-%m-%d %H:%M')}")
        
        # Sort by composite score (distance + availability + rating)
        recommendations.sort(key=lambda x: (x.distance_km * 0.3 + (5.0 - x.rating) * 0.3 + 
                                          (x.next_available - datetime.datetime.now()).days * 0.4))
        
        print(f"   🏆 Top recommendation: Dr. {recommendations[0].name}")
        
        return recommendations
    
    def _calculate_distance(self, patient_location: str, physician_location: str) -> float:
        """Calculate approximate distance between locations"""
        # Extract city names (simplified)
        patient_city = next((city for city in LOCATION_COORDS.keys() if city in patient_location), "New York")
        physician_city = next((city for city in LOCATION_COORDS.keys() if city in physician_location), "New York")
        
        if patient_city == physician_city:
            return round(5.0 + hash(patient_location + physician_location) % 20, 1)  # 5-25 km within city
        else:
            # Simplified inter-city distance
            return round(200.0 + hash(patient_city + physician_city) % 1000, 1)
    
    def _calculate_next_availability(self, physician: Dict, urgency: UrgencyLevel) -> datetime.datetime:
        """Calculate next available appointment based on urgency"""
        now = datetime.datetime.now()
        
        if urgency == UrgencyLevel.CRITICAL:
            return now + datetime.timedelta(minutes=30)  # Emergency slot
        elif urgency == UrgencyLevel.URGENT:
            return now + datetime.timedelta(hours=2)
        elif urgency == UrgencyLevel.SEMI_URGENT:
            return now + datetime.timedelta(days=1)
        elif urgency == UrgencyLevel.STANDARD:
            return now + datetime.timedelta(days=7)
        else:
            return now + datetime.timedelta(days=30)