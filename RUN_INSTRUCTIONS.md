# Student Health Assistant - Run Instructions

This document provides instructions on how to run the Student Health Assistant application.

## Prerequisites

1. Python 3.10 installed
2. Virtual environment for Python (recommended)
3. Git (for version control)

## Setup

1. Clone the repository or navigate to the project folder
2. Set up virtual environments for Rasa and Django (if not already created)

## Running the Backend Server

The Django backend provides APIs for disease prediction and user management.

1. Navigate to the backend directory:
   ```
   cd student_health_assistant/backend
   ```

2. Activate your virtual environment (if using one)

3. Install requirements (if not already installed):
   ```
   pip install -r requirements.txt
   ```

4. Run the Django server using the start script:
   ```
   ./start_django.sh
   ```
   
   Or manually:
   ```
   python manage.py runserver
   ```

5. The server will be available at http://localhost:8000

## Running the Rasa Chatbot Server

The Rasa server handles chatbot interactions and natural language processing.

1. Navigate to the Rasa app directory:
   ```
   cd student_health_assistant/rasa_app
   ```

2. Activate your virtual environment (if using one)

3. Install requirements (if not already installed):
   ```
   pip install -r requirements.txt
   ```

4. Run the Rasa server using the start script:
   ```
   ./start_rasa.sh
   ```
   
   Or manually:
   ```
   rasa run --enable-api --cors "*"
   ```

5. In a separate terminal, start the Rasa action server:
   ```
   rasa run actions
   ```

6. The Rasa server will be available at http://localhost:5005

## Testing the System

You can use the test script to verify that all components are running correctly:

```
python student_health_assistant/test_api_endpoints.py
```

This will check all API endpoints and report their status.

## Troubleshooting

If you encounter any issues:

1. **Django API errors (404)**:
   - Make sure Django server is running
   - Verify that the health_app.urls contains the necessary endpoints

2. **Rasa Health Check errors (404)**:
   - Ensure Rasa is running with the `--enable-api` flag
   - Check that the Rasa action server is running

3. **Rasa not responding to messages**:
   - Check that the model is trained properly
   - Verify that the action server is running correctly

4. **Permission Issues with Start Scripts**:
   - If you can't run the start scripts, make them executable:
     ```
     chmod +x start_django.sh start_rasa.sh
     ``` 