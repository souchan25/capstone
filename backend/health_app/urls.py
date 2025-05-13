from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    StudentRegistrationView, StudentProfileView, ConsentUpdateView,
    SymptomSubmissionView, StudentReportHistoryView, ClinicDashboardView,
    RasaWebhookView, HealthCheckView, predict_disease
)
from .auth import CustomAuthToken

urlpatterns = [
    # Health check endpoint
    path('health/', HealthCheckView.as_view(), name='health_check'),
    
    # Direct disease prediction endpoint
    path('predict-disease/', predict_disease, name='predict_disease'),
    
    # Authentication endpoints - these should be accessible to anyone
    path('token/', CustomAuthToken.as_view(), name='token_obtain'),
    path('register/', StudentRegistrationView.as_view(), name='register'),
    
    # Student endpoints - protected by authentication
    path('profile/', StudentProfileView.as_view(), name='student_profile'),
    path('user/profile/', StudentProfileView.as_view(), name='user_profile'),
    path('update-consent/', ConsentUpdateView.as_view(), name='update_consent'),
    path('submit-symptoms/', SymptomSubmissionView.as_view(), name='submit_symptoms'),
    path('history/', StudentReportHistoryView.as_view(), name='student_history'),
    
    # Clinic staff endpoints
    path('clinic/dashboard/', ClinicDashboardView.as_view(), name='clinic_dashboard'),
    
    # Rasa webhook
    path('rasa-webhook/', RasaWebhookView.as_view(), name='rasa_webhook'),
] 