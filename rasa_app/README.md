# Student Health Assistant - Rasa Chatbot

This is the Rasa chatbot component of the Student Health Assistant application. It provides the conversational interface for users to describe their symptoms and receive potential diagnoses.

## Setup Requirements

- Python 3.10
- Rasa 3.x
- Access to a Django backend API for disease prediction

## Project Structure

- `data/` - Contains training data for the Rasa model
  - `nlu.yml` - Natural language understanding training examples
  - `stories.yml` - Conversation flow examples
  - `rules.yml` - Conversation rules
- `actions/` - Custom actions that interact with external systems
  - `actions.py` - Contains the implementation for disease diagnosis
- `domain.yml` - Defines intents, entities, slots, and responses
- `config.yml` - Configuration for NLU and Core models
- `endpoints.yml` - Endpoints configuration for action server
- `train_test.py` - Helper script for training and testing

## How It Works

1. User interacts with the chatbot, describing their symptoms
2. Rasa extracts symptom entities from the user's message
3. The custom action calls the Django backend API to get a disease prediction
4. The prediction is presented back to the user

### Disease and Symptom Information

The chatbot can also provide:
- Information about diseases when asked "What is [disease]?"
- Information about symptoms when asked "What is [symptom]?"
- Appropriate responses to questions like "Am I experiencing [symptom]?" or "Do I have [disease]?"

This feature uses knowledge datasets from:
- `Data/Knowledge/disease.json` - Contains information about diseases, their descriptions, and advice
- `Data/Knowledge/symptoms.json` - Contains information about symptoms and their descriptions

## Symptom Entity Recognition

The chatbot uses a comprehensive symptom dataset to recognize and normalize symptom mentions in user messages. This includes:

- Direct symptom recognition
- Fuzzy matching for similar terms
- Lookup tables for common symptoms

## Running the Application

### Training the Model

```bash
python train_test.py train
# or directly:
rasa train
```

### Starting the Action Server

```bash
python train_test.py actions
# or directly:
rasa run actions
```

### Running the Chatbot

```bash
python train_test.py shell  # For interactive shell testing
# or directly:
rasa shell  # For testing in the terminal

# For web/API interactions:
rasa run --enable-api --cors "*"
```

### Testing the NLU Model

```bash
python train_test.py test
# or directly:
rasa test nlu
```

## Integration with Django Backend

The chatbot calls the Django backend API at `http://localhost:8000/api/predict-disease/` with a JSON payload containing the normalized symptoms. Make sure the Django backend is running before testing the chatbot's diagnosis capability.

Example API call:
```json
{
  "symptoms": ["headache", "fever", "cough"]
}
```

Expected response:
```json
{
  "disease": "Common Cold",
  "confidence": 0.85
}
``` 