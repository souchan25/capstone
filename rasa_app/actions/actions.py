# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
import logging
import os
import re
from difflib import get_close_matches

logger = logging.getLogger(__name__)

class ActionDiagnoseDisease(Action):
    def __init__(self):
        super().__init__()
        # Load symptoms from JSON file
        self.symptoms_data = []
        self.symptom_names = []
        try:
            # Use the actual path to the symptoms.json file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            symptoms_path = os.path.join(base_dir, 'Data', 'Knowledge', 'symptoms.json')
            logger.info(f"Looking for symptoms file at: {symptoms_path}")
            with open(symptoms_path, 'r') as f:
                self.symptoms_data = json.load(f)
                self.symptom_names = [item['symptom'].lower() for item in self.symptoms_data]
            logger.info(f"Loaded {len(self.symptom_names)} symptoms from dataset")
        except Exception as e:
            logger.error(f"Error loading symptoms data: {str(e)}")
            # Fallback to hard-coded common symptoms if file loading fails
            self.symptom_names = [
                "headache", "fever", "nausea", "cough", "sore throat", "fatigue",
                "chest pain", "shortness of breath", "rash", "joint pain"
            ]
    
    def name(self) -> Text:
        return "action_diagnose_disease"
    
    def normalize_symptom(self, symptom_text: str) -> str:
        """Match user input to closest symptom in the dataset"""
        symptom_text = symptom_text.lower().strip()
        
        # Direct match
        if symptom_text in self.symptom_names:
            return symptom_text
        
        # Find closest match
        matches = get_close_matches(symptom_text, self.symptom_names, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        
        # Try partial matching
        for name in self.symptom_names:
            if symptom_text in name or name in symptom_text:
                return name
        
        # If no match found, return original
        return symptom_text

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract symptoms from slots
        symptoms = tracker.get_slot('symptoms')
        
        if not symptoms:
            # Extract all symptom entities manually from the conversation
            symptoms = []
            for event in tracker.events:
                if event.get('event') == 'user' and event.get('parse_data'):
                    for entity in event.get('parse_data', {}).get('entities', []):
                        if entity.get('entity') == 'symptom':
                            symptoms.append(entity.get('value'))
        
        if not symptoms or len(symptoms) == 0:
            dispatcher.utter_message(text="I couldn't identify any symptoms. Please tell me what symptoms you're experiencing.")
            return []
        
        # Normalize symptoms to match dataset
        normalized_symptoms = [self.normalize_symptom(s) for s in symptoms]
        normalized_symptoms = list(set(normalized_symptoms))  # Remove duplicates
        
        # Debug log
        logger.info(f"Original symptoms: {symptoms}")
        logger.info(f"Normalized symptoms: {normalized_symptoms}")
        
        try:
            # Call Django backend API for prediction
            response = requests.post(
                "http://localhost:8000/api/predict-disease/",
                json={"symptoms": normalized_symptoms},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                prediction_data = response.json()
                disease = prediction_data.get('disease')
                confidence = prediction_data.get('confidence', 0) * 100  # Convert to percentage
                
                message = f"Based on your symptoms, you may have {disease} (confidence: {confidence:.1f}%).\n\n"
                message += "Please note that this is not a professional medical diagnosis. "
                message += "For accurate diagnosis and treatment, please consult a healthcare professional."
                
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="I'm having trouble connecting to the diagnostic system. Please try again later.")
                logger.error(f"Backend API error: {response.status_code} - {response.text}")
        
        except Exception as e:
            dispatcher.utter_message(text="I'm having trouble processing your symptoms right now. Please try again later.")
            logger.error(f"Error in disease prediction: {str(e)}")
        
        return [SlotSet("symptoms", normalized_symptoms)]

class ActionProvideDiseaseInfo(Action):
    def __init__(self):
        super().__init__()
        # Load disease information
        self.diseases_data = []
        self.disease_names = []
        try:
            # Use the actual path to the disease.json file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            diseases_path = os.path.join(base_dir, 'Data', 'Knowledge', 'disease.json')
            logger.info(f"Looking for diseases file at: {diseases_path}")
            with open(diseases_path, 'r') as f:
                self.diseases_data = json.load(f)
                self.disease_names = [item['disease'].lower() for item in self.diseases_data]
            logger.info(f"Loaded {len(self.disease_names)} diseases from dataset")
        except Exception as e:
            logger.error(f"Error loading diseases data: {str(e)}")
            # Fallback to common diseases if file loading fails
            self.diseases_data = [
                {"disease": "Common cold", "description": "A viral infection of the upper respiratory tract.", "advice": "Rest and stay hydrated."},
                {"disease": "COVID-19", "description": "A respiratory illness caused by the SARS-CoV-2 virus.", "advice": "Isolate and contact healthcare."}
            ]
            self.disease_names = [item['disease'].lower() for item in self.diseases_data]
    
    def name(self) -> Text:
        return "action_provide_disease_info"
    
    def normalize_disease_name(self, disease_text: str) -> str:
        """Match user query to closest disease in the dataset"""
        disease_text = disease_text.lower().strip()
        
        # Direct match
        if disease_text in self.disease_names:
            return disease_text
        
        # Find closest match
        matches = get_close_matches(disease_text, self.disease_names, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        
        # Try partial matching
        for name in self.disease_names:
            if disease_text in name or name in disease_text:
                return name
        
        return None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract disease entity
        disease = next(tracker.get_latest_entity_values("disease"), None)
        
        if not disease:
            dispatcher.utter_message(text="I'm not sure which disease you're asking about. Could you please specify?")
            return []
        
        normalized_disease = self.normalize_disease_name(disease)
        logger.info(f"Looking up disease info for: {disease} (normalized: {normalized_disease})")
        
        if normalized_disease:
            # Find disease info in the dataset
            disease_info = None
            for item in self.diseases_data:
                if item['disease'].lower() == normalized_disease:
                    disease_info = item
                    break
            
            if disease_info:
                # Format and send the information
                response = f"**{disease_info['disease']}**\n\n"
                response += f"{disease_info['description']}\n\n"
                if 'advice' in disease_info:
                    response += f"**Advice:** {disease_info['advice']}"
                
                dispatcher.utter_message(text=response)
                return [SlotSet("disease", normalized_disease)]
        
        # If disease not found
        dispatcher.utter_message(text=f"I don't have detailed information about {disease}. Please consult a healthcare professional for information about this condition.")
        return []

class ActionProvideSymptomInfo(Action):
    def __init__(self):
        super().__init__()
        # Load symptom information
        self.symptoms_data = []
        self.symptom_names = []
        try:
            # Use the actual path to the symptoms.json file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            symptoms_path = os.path.join(base_dir, 'Data', 'Knowledge', 'symptoms.json')
            logger.info(f"Looking for symptoms file at: {symptoms_path}")
            with open(symptoms_path, 'r') as f:
                self.symptoms_data = json.load(f)
                self.symptom_names = [item['symptom'].lower() for item in self.symptoms_data]
            logger.info(f"Loaded {len(self.symptom_names)} symptoms from dataset")
        except Exception as e:
            logger.error(f"Error loading symptoms data: {str(e)}")
            # Fallback
            self.symptoms_data = [
                {"symptom": "headache", "description": "Pain in the head."},
                {"symptom": "fever", "description": "Elevated body temperature."}
            ]
            self.symptom_names = [item['symptom'].lower() for item in self.symptoms_data]
    
    def name(self) -> Text:
        return "action_provide_symptom_info"
    
    def normalize_symptom(self, symptom_text: str) -> str:
        """Match user query to closest symptom in the dataset"""
        symptom_text = symptom_text.lower().strip()
        
        # Direct match
        if symptom_text in self.symptom_names:
            return symptom_text
        
        # Find closest match
        matches = get_close_matches(symptom_text, self.symptom_names, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        
        # Try partial matching
        for name in self.symptom_names:
            if symptom_text in name or name in symptom_text:
                return name
        
        return None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract symptom entity
        symptom = next(tracker.get_latest_entity_values("symptom"), None)
        
        if not symptom:
            dispatcher.utter_message(text="I'm not sure which symptom you're asking about. Could you please specify?")
            return []
        
        normalized_symptom = self.normalize_symptom(symptom)
        logger.info(f"Looking up symptom info for: {symptom} (normalized: {normalized_symptom})")
        
        if normalized_symptom:
            # Find symptom info in the dataset
            symptom_info = None
            for item in self.symptoms_data:
                if item['symptom'].lower() == normalized_symptom:
                    symptom_info = item
                    break
            
            if symptom_info:
                # Format and send the information
                response = f"**{symptom_info['symptom']}**\n\n"
                response += f"{symptom_info['description']}"
                
                dispatcher.utter_message(text=response)
                return [SlotSet("symptom", normalized_symptom)]
        
        # If symptom not found
        dispatcher.utter_message(text=f"I don't have detailed information about '{symptom}'. Please consult a healthcare professional about this symptom.")
        return []

class ActionCheckIfExperiencing(Action):
    def name(self) -> Text:
        return "action_check_if_experiencing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract symptom or disease entity
        symptom = next(tracker.get_latest_entity_values("symptom"), None)
        disease = next(tracker.get_latest_entity_values("disease"), None)
        
        if symptom:
            response = "I can't determine if you're experiencing a specific symptom based just on our conversation. "
            response += "To better understand your situation, please tell me about all your symptoms, and I can help analyze them. "
            response += "Remember, I can provide information but not a medical diagnosis."
            dispatcher.utter_message(text=response)
        
        elif disease:
            response = "I can't diagnose whether you have a specific condition. "
            response += "If you tell me your symptoms, I can help analyze them and provide general information. "
            response += "For a proper diagnosis, please consult a healthcare professional."
            dispatcher.utter_message(text=response)
        
        else:
            dispatcher.utter_message(text="I'm not sure what you're asking about. Please describe your symptoms so I can try to help.")
        
        return []

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
