from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import Student, SymptomReport, PredictionRecord
from .serializers import (
    UserSerializer, UserProfileSerializer, StudentSerializer, StudentRegistrationSerializer,
    SymptomReportSerializer, PredictionRecordSerializer,
    SymptomInputSerializer, ConsentUpdateSerializer
)
from .predictor import predictor
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
from collections import Counter

class IsClinicStaff(permissions.BasePermission):
    """
    Custom permission to only allow clinic staff to access resource.
    Assumes clinic staff are marked as staff in Django User model.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class StudentRegistrationView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            # Log the registration attempt
            print(f"Registration attempt with data: {request.data}")
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Create the user and student profile
                user = serializer.save()
                
                # Generate auth token
                token, created = Token.objects.get_or_create(user=user)
                
                # Return success response with token
                return Response({
                    "message": "Registration successful",
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email
                }, status=status.HTTP_201_CREATED)
            else:
                # Return validation errors
                return Response({
                    "error": "Registration failed",
                    "detail": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            # Log the error
            print(f"Registration error: {str(e)}")
            return Response({
                "error": "Registration failed",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Student.objects.get(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileSerializer
        return StudentSerializer
    
    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Re-fetch the student to return the updated profile
            student = Student.objects.get(user=user)
            return Response(StudentSerializer(student).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsentUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ConsentUpdateSerializer(data=request.data)
        if serializer.is_valid():
            student = Student.objects.get(user=request.user)
            student.share_data_consent = serializer.validated_data['share_data_consent']
            student.save()
            return Response({'status': 'consent updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SymptomSubmissionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = SymptomInputSerializer(data=request.data)
        if serializer.is_valid():
            # Create a symptom report
            student = Student.objects.get(user=request.user)
            symptom_report = SymptomReport.objects.create(
                student=student,
                symptoms=serializer.validated_data['symptoms'],
                input_method=serializer.validated_data['input_method']
            )
            
            # Get prediction from the model
            prediction_result = predictor.predict(serializer.validated_data['symptoms'])
            
            # Create a prediction record
            prediction_record = PredictionRecord.objects.create(
                symptom_report=symptom_report,
                disease=prediction_result['disease'],
                confidence_score=prediction_result['confidence_score'],
                advice=prediction_result['advice'],
                severity=prediction_result['severity']
            )
            
            # Return the prediction record
            return Response({
                'disease': prediction_record.disease,
                'confidence': prediction_record.confidence_score,
                'advice': prediction_record.advice,
                'severity': prediction_record.severity
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentReportHistoryView(generics.ListAPIView):
    serializer_class = SymptomReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return SymptomReport.objects.filter(student=student).order_by('-created_at')

class ClinicDashboardView(generics.ListAPIView):
    serializer_class = SymptomReportSerializer
    permission_classes = [IsClinicStaff]
    
    def get_queryset(self):
        # Only show reports from students who have consented
        return SymptomReport.objects.filter(
            student__share_data_consent=True
        ).order_by('-created_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Include prediction records in the response
        context.update({"include_predictions": True})
        return context

class RasaWebhookView(APIView):
    """
    Webhook for Rasa to get disease predictions
    """
    permission_classes = [permissions.AllowAny]  # Allow Rasa to access without authentication
    
    def post(self, request):
        # Extract symptoms from Rasa request
        try:
            symptoms = request.data.get('symptoms', [])
            if not symptoms:
                return Response(
                    {"error": "No symptoms provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get prediction
            prediction_result = predictor.predict(symptoms)
            
            # Return prediction to Rasa
            return Response(prediction_result)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HealthCheckView(APIView):
    """
    Simple health check endpoint to verify the API is working
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            "status": "ok",
            "message": "Health check passed",
            "service": "Student Health Assistant API"
        })

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def predict_disease(request):
    """
    Direct disease prediction endpoint, not requiring authentication
    Useful for testing and external integrations
    """
    try:
        symptoms = request.data.get('symptoms', [])
        if not symptoms:
            return Response(
                {"error": "No symptoms provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get prediction
        prediction_result = predictor.predict(symptoms)
        
        # Return prediction
        return Response({
            'disease': prediction_result['disease'],
            'confidence': prediction_result['confidence_score'],
            'advice': prediction_result['advice'],
            'severity': prediction_result['severity']
        })
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_stats(request):
    """API endpoint to provide statistics for the admin dashboard"""
    today = timezone.now().date()
    
    # Count reports by date (last 7 days)
    start_date = today - timedelta(days=6)
    reports_by_date = {}
    for i in range(7):
        date = start_date + timedelta(days=i)
        reports_by_date[date.strftime('%Y-%m-%d')] = 0
    
    recent_reports = SymptomReport.objects.filter(created_at__date__gte=start_date)
    for report in recent_reports:
        date_str = report.created_at.date().strftime('%Y-%m-%d')
        if date_str in reports_by_date:
            reports_by_date[date_str] += 1
    
    # Count symptoms
    all_symptoms = []
    for report in recent_reports:
        all_symptoms.extend(report.symptoms)
    
    symptom_counts = Counter(all_symptoms).most_common(6)
    
    # Count by severity
    severity_counts = Counter([p.severity for p in PredictionRecord.objects.all()])
    
    return Response({
        'counts': {
            'total_reports': SymptomReport.objects.count(),
            'total_students': Student.objects.count(),
            'today_reports': SymptomReport.objects.filter(created_at__date=today).count(),
            'high_severity': PredictionRecord.objects.filter(severity='HIGH').count(),
        },
        'charts': {
            'reports_by_date': reports_by_date,
            'symptoms': {
                'labels': [s[0] for s in symptom_counts],
                'data': [s[1] for s in symptom_counts],
            },
            'severity': {
                'labels': list(severity_counts.keys()),
                'data': list(severity_counts.values()),
            }
        }
    })
