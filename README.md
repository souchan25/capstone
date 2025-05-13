# Student Health Assistant

A system that combines machine learning with a user-friendly interface to help students identify possible health conditions based on their symptoms. It includes a chatbot interface and a symptom form for input, along with a clinic dashboard for university clinic staff.

## Features

- User authentication (registration and login)
- Symptom input via form or chat interface
- Machine learning-based disease prediction
- Severity assessment
- Consent management for data sharing
- Clinic dashboard for university staff

## Project Structure

```
student_health_assistant/
├── backend/             # Django backend
│   ├── health_app/      # Main Django app
│   ├── health_project/  # Django project settings
│   └── manage.py        # Django management script
├── frontend/            # Vue.js frontend
│   ├── public/
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── router/      # Vue router
│   │   ├── App.vue      # Main app component
│   │   └── main.js      # App entry point
│   └── package.json     # Frontend dependencies
└── README.md            # This file
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd student_health_assistant/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create database migrations:
```bash
python manage.py makemigrations health_app
python manage.py migrate
```

5. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The backend API will be available at http://localhost:8000/api/

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd student_health_assistant/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run serve
```

The frontend will be available at http://localhost:8080/

## Usage

1. Access the application at http://localhost:8080/
2. Register a new account or login
3. Use either the symptom form or chat interface to describe your symptoms
4. View your predicted condition with advice
5. Staff members can access the clinic dashboard at http://localhost:8080/clinic-dashboard

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: Vue.js
- **Machine Learning**: scikit-learn
- **Authentication**: JWT tokens
- **Database**: SQLite (development)

## License

MIT 