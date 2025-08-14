from typing import Dict, List
import openai
from models import SymptomAssessment, TriageResult, UrgencyLevel
from config import LLM_MODEL, SPECIALTY_KEYWORDS

class TriageAgent:
    async def perform_triage(self, assessment: SymptomAssessment, context: Dict, rag_system) -> TriageResult:
        """Perform intelligent medical triage using RAG and context"""
        print("   🔬 Analyzing symptoms with medical knowledge base...")
        
        # Retrieve relevant medical knowledge
        symptoms_text = f"{assessment.primary_complaint} {' '.join(assessment.symptoms)}"
        medical_knowledge = await rag_system.retrieve_medical_knowledge(symptoms_text, context["demographic"])
        
        # AI-powered triage decision
        triage_prompt = self._build_triage_prompt(assessment, context, medical_knowledge)
        
        print("   🧠 Consulting AI for clinical decision making...")
        
        try:
            response = openai.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": triage_prompt}],
                temperature=0.1
            )
            
            ai_assessment = response.choices[0].message.content
            print(f"   💡 AI Assessment completed")
            
        except Exception as e:
            print(f"   ❌ AI consultation failed: {e}")
            ai_assessment = "Fallback assessment based on symptoms and risk factors"
        
        # Determine urgency level
        urgency_level = self._determine_urgency(assessment, context, medical_knowledge)
        print(f"   ⚡ Urgency Level: {urgency_level.value}")
        
        # Recommend specialty
        specialty = self._recommend_specialty(assessment, medical_knowledge)
        print(f"   🏥 Recommended Specialty: {specialty}")
        
        # Calculate confidence score
        confidence = self._calculate_confidence(context, medical_knowledge)
        print(f"   📊 Confidence Score: {confidence:.2f}")
        
        return TriageResult(
            assessment_id=assessment.assessment_id,
            urgency_level=urgency_level,
            recommended_specialty=specialty,
            risk_factors=context["risk"]["risk_factors"],
            clinical_reasoning=ai_assessment[:200] + "..." if len(ai_assessment) > 200 else ai_assessment,
            confidence_score=confidence,
            requires_emergency=urgency_level == UrgencyLevel.CRITICAL,
            estimated_wait_time=self._estimate_wait_time(urgency_level)
        )
    
    def _build_triage_prompt(self, assessment: SymptomAssessment, context: Dict, knowledge: List[Dict]) -> str:
        """Build comprehensive triage prompt for AI"""
        prompt = f"""
        You are an experienced emergency medicine physician performing patient triage.
        
        PATIENT INFORMATION:
        - Age: {context['demographic']['age']}
        - Gender: {context['demographic']['gender']}
        - Primary Complaint: {assessment.primary_complaint}
        - Symptoms: {', '.join(assessment.symptoms)}
        - Severity (1-10): {assessment.severity}
        - Duration: {assessment.duration}
        - Medical History: {', '.join(context['medical']['chronic_conditions'])}
        - Current Medications: {', '.join(context['medical']['current_medications'])}
        - Allergies: {', '.join(context['medical']['allergies'])}
        
        RELEVANT CLINICAL GUIDELINES:
        """
        
        for kb in knowledge:
            prompt += f"\n- {kb['title']}: {kb['content']}"
        
        prompt += f"""
        
        RISK FACTORS:
        {', '.join(context['risk']['risk_factors'])}
        
        Please provide a brief clinical assessment focusing on:
        1. Most likely diagnosis or differential
        2. Risk stratification
        3. Urgency level recommendation
        4. Red flags to watch for
        
        Keep response concise and clinical.
        """
        
        return prompt
    
    def _determine_urgency(self, assessment: SymptomAssessment, context: Dict, knowledge: List[Dict]) -> UrgencyLevel:
        """Determine urgency level based on multiple factors"""
        urgency_score = 0
        
        # Severity contribution
        urgency_score += assessment.severity * 10
        
        # Risk factors contribution
        urgency_score += len(context["risk"]["risk_factors"]) * 15
        
        # Age factors
        if context["demographic"]["age"] < 2 or context["demographic"]["age"] > 80:
            urgency_score += 20
        
        # Symptom-based red flags
        red_flags = ["chest pain", "difficulty breathing", "severe headache", "loss of consciousness"]
        for symptom in assessment.symptoms:
            if any(flag in symptom.lower() for flag in red_flags):
                urgency_score += 30
        
        # Knowledge base urgency indicators
        for kb in knowledge:
            if kb.get("urgency") == "high":
                urgency_score += 25
            elif kb.get("urgency") == "medium":
                urgency_score += 15
        
        # Duration factors
        if "sudden" in assessment.duration.lower() or "acute" in assessment.duration.lower():
            urgency_score += 20
        
        print(f"   📊 Calculated urgency score: {urgency_score}")
        
        # Map score to urgency level
        if urgency_score >= 100:
            return UrgencyLevel.CRITICAL
        elif urgency_score >= 70:
            return UrgencyLevel.URGENT
        elif urgency_score >= 50:
            return UrgencyLevel.SEMI_URGENT
        elif urgency_score >= 30:
            return UrgencyLevel.STANDARD
        else:
            return UrgencyLevel.NON_URGENT
    
    def _recommend_specialty(self, assessment: SymptomAssessment, knowledge: List[Dict]) -> str:
        """Recommend medical specialty based on symptoms and knowledge"""
        # Extract specialties from retrieved knowledge
        specialties_found = [kb.get("specialty", "general") for kb in knowledge]
        
        if specialties_found:
            # Return most relevant specialty
            specialty_counts = {}
            for spec in specialties_found:
                specialty_counts[spec] = specialty_counts.get(spec, 0) + 1
            
            recommended = max(specialty_counts, key=specialty_counts.get)
            print(f"   🎯 Specialty recommendation based on knowledge: {recommended}")
            return recommended
        
        # Fallback to symptom-based matching
        symptom_text = f"{assessment.primary_complaint} {' '.join(assessment.symptoms)}".lower()
        
        for specialty, keywords in SPECIALTY_KEYWORDS.items():
            if any(keyword in symptom_text for keyword in keywords):
                print(f"   🎯 Specialty recommendation based on symptoms: {specialty}")
                return specialty
        
        print("   🎯 Defaulting to general medicine")
        return "general_medicine"
    
    def _calculate_confidence(self, context: Dict, knowledge: List[Dict]) -> float:
        """Calculate confidence score for the triage decision"""
        confidence = 0.5  # Base confidence
        
        # Knowledge retrieval quality
        if knowledge:
            avg_score = sum(kb.get("score", 0.5) for kb in knowledge) / len(knowledge)
            confidence += avg_score * 0.3
        
        # Context completeness
        context_completeness = (
            len(context["medical"]["chronic_conditions"]) > 0,
            len(context["medical"]["current_medications"]) > 0,
            context["symptom"]["severity"] > 0,
            len(context["risk"]["risk_factors"]) >= 0
        )
        confidence += sum(context_completeness) / len(context_completeness) * 0.2
        
        return min(1.0, confidence)
    
    def _estimate_wait_time(self, urgency: UrgencyLevel) -> str:
        """Estimate wait time based on urgency level"""
        wait_times = {
            UrgencyLevel.CRITICAL: "Immediate",
            UrgencyLevel.URGENT: "Within 2 hours",
            UrgencyLevel.SEMI_URGENT: "Within 24 hours", 
            UrgencyLevel.STANDARD: "Within 1-2 weeks",
            UrgencyLevel.NON_URGENT: "Within 1 month"
        }
        return wait_times[urgency]