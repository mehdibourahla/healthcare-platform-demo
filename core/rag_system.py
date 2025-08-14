import streamlit as st
from typing import Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import openai
import logging

from config import (
    EMBEDDINGS_MODEL, MEDICAL_GUIDELINES
)

logger = logging.getLogger(__name__)

class MedicalKnowledgeRAG:
    def __init__(self, qdrant_client: Optional[QdrantClient]):
        self.client = qdrant_client
        self.collection_name = "medical_knowledge"
        self.embeddings_model = EMBEDDINGS_MODEL
        self._setup_collections()
        
    def _setup_collections(self):
        """Initialize vector collections"""
        if not self.client:
            st.warning("Qdrant client not available. Using fallback mode.")
            return
            
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
                )
                self._populate_medical_knowledge()
                st.info("🏥 Medical knowledge base initialized")
            
        except Exception as e:
            st.warning(f"Qdrant setup issue: {e}. Using fallback mode.")
    
    def _populate_medical_knowledge(self):
        """Populate with sample medical knowledge"""
        points = []
        for i, guideline in enumerate(MEDICAL_GUIDELINES):
            try:
                # Get embedding for the content
                response = openai.embeddings.create(
                    model=self.embeddings_model,
                    input=f"{guideline['title']} {guideline['content']}"
                )
                embedding = response.data[0].embedding
                
                point = PointStruct(
                    id=i,
                    vector=embedding,
                    payload=guideline
                )
                points.append(point)
            except Exception as e:
                st.warning(f"Error creating embedding: {e}")
        
        if points:
            try:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                print("✅ Medical knowledge base populated successfully")
            except Exception as e:
                st.warning(f"Error upserting to Qdrant: {e}")
    
    async def retrieve_medical_knowledge(self, symptoms: str, patient_context: Dict) -> List[Dict]:
        """Retrieve relevant medical guidelines based on symptoms"""
        print(f"\n🔍 RAG RETRIEVAL:")
        print(f"   Query: {symptoms}")
        print(f"   Patient Context: Age {patient_context.get('age')}, Gender {patient_context.get('gender')}")
        
        if not self.client:
            return self._fallback_retrieval(symptoms)
            
        try:
            # Create embedding for the query
            response = openai.embeddings.create(
                model=self.embeddings_model,
                input=symptoms
            )
            query_embedding = response.data[0].embedding
            
            # Search for relevant medical knowledge
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=3
            )
            
            retrieved_knowledge = []
            for result in search_results:
                retrieved_knowledge.append({
                    "title": result.payload["title"],
                    "content": result.payload["content"],
                    "specialty": result.payload["specialty"],
                    "urgency": result.payload["urgency"],
                    "score": result.score
                })
                print(f"   📚 Retrieved: {result.payload['title']} (score: {result.score:.3f})")
            
            print(f"   ✅ Retrieved {len(retrieved_knowledge)} relevant guidelines")
            return retrieved_knowledge
            
        except Exception as e:
            print(f"   ❌ RAG retrieval failed: {e}")
            # Fallback to rule-based retrieval
            return self._fallback_retrieval(symptoms)
    
    def _fallback_retrieval(self, symptoms: str) -> List[Dict]:
        """Fallback knowledge retrieval when Qdrant fails"""
        print("   🔄 Using fallback knowledge retrieval")
        
        fallback_knowledge = {
            "chest pain": {
                "title": "Chest Pain Emergency Protocol",
                "content": "Immediate cardiac evaluation required. Check for STEMI, unstable angina.",
                "specialty": "cardiology",
                "urgency": "high"
            },
            "headache": {
                "title": "Headache Assessment",
                "content": "Evaluate for secondary causes. Consider imaging for red flags.",
                "specialty": "neurology", 
                "urgency": "medium"
            },
            "abdominal pain": {
                "title": "Abdominal Pain Triage",
                "content": "Rule out surgical emergencies. Consider appendicitis, bowel obstruction.",
                "specialty": "general_surgery",
                "urgency": "high"
            }
        }
        
        symptoms_lower = symptoms.lower()
        retrieved = []
        
        for symptom, knowledge in fallback_knowledge.items():
            if symptom in symptoms_lower:
                retrieved.append({
                    "title": knowledge["title"],
                    "content": knowledge["content"], 
                    "specialty": knowledge["specialty"],
                    "urgency": knowledge["urgency"],
                    "score": 0.8
                })
        
        return retrieved if retrieved else [list(fallback_knowledge.values())[0]]