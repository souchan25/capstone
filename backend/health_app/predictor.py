import os
import pickle
import json
import numpy as np
from django.conf import settings

class DiseasePredictor:
    def __init__(self):
        # Set paths to model files
        base_dir = settings.BASE_DIR
        model_dir = os.path.join(os.path.dirname(base_dir), '..', 'Model')
        data_dir = os.path.join(os.path.dirname(base_dir), '..', 'Data')
        
        # Load models
        self.vectorizer = pickle.load(open(os.path.join(model_dir, 'symptom_vectorizer.pkl'), 'rb'))
        self.classifier = pickle.load(open(os.path.join(model_dir, 'disease_classifier.pkl'), 'rb'))
        self.model = pickle.load(open(os.path.join(model_dir, 'disease_model.pkl'), 'rb'))
        
        # Load disease dataset for advice
        with open(os.path.join(data_dir, 'disease_dataset.json'), 'r') as f:
            self.disease_data = json.load(f)
    
    def predict(self, symptoms):
        """
        Predict disease based on symptoms
        Args:
            symptoms: list of symptom strings
        Returns:
            dict with disease name, confidence score, advice, and severity
        """
        # Convert symptoms to lowercase
        symptoms = [s.lower() for s in symptoms]
        
        # Vectorize the symptoms
        symptom_vector = self.vectorizer.transform([' '.join(symptoms)])
        
        # Predict disease
        prediction = self.classifier.predict(symptom_vector)
        prediction_proba = self.classifier.predict_proba(symptom_vector)
        max_proba = max(prediction_proba[0])
        disease = prediction[0]
        
        # Get advice for the predicted disease
        advice = ""
        for disease_info in self.disease_data:
            if disease_info["disease"].lower() == disease.lower():
                advice = disease_info["advice"]
                break
        
        # Determine severity based on confidence score and symptoms
        severity = self._assess_severity(disease, symptoms, max_proba)
        
        return {
            "disease": disease,
            "confidence_score": float(max_proba),
            "advice": advice,
            "severity": severity
        }
    
    def _assess_severity(self, disease, symptoms, confidence):
        """
        Assess severity of the condition based on disease, symptoms and confidence
        """
        # High severity symptoms
        high_severity_symptoms = [
            "difficulty breathing", "chest pain", "severe headache", 
            "loss of consciousness", "sudden numbness", "shortness of breath"
        ]
        
        # Check if any symptoms are high severity
        for symptom in symptoms:
            if any(high_sev in symptom for high_sev in high_severity_symptoms):
                return "HIGH"
        
        # If confidence is very low, recommend a doctor visit (medium severity)
        if confidence < 0.4:
            return "MEDIUM"
            
        # Set severity based on disease type
        high_severity_diseases = [
            "pneumonia", "stroke", "heart attack", "meningitis", "appendicitis"
        ]
        
        if any(h_disease.lower() in disease.lower() for h_disease in high_severity_diseases):
            return "HIGH"
            
        medium_severity_diseases = [
            "influenza", "covid-19", "urinary tract infection", "bronchitis"
        ]
        
        if any(m_disease.lower() in disease.lower() for m_disease in medium_severity_diseases):
            return "MEDIUM"
            
        return "LOW"

# Create a singleton instance
predictor = DiseasePredictor() 