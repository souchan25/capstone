from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    share_data_consent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.school_id})"

class SymptomReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    symptoms = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    input_method = models.CharField(
        max_length=10, 
        choices=[("CHAT", "Chat"), ("FORM", "Form")],
        default="FORM"
    )

    def __str__(self):
        return f"Report by {self.student.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class PredictionRecord(models.Model):
    symptom_report = models.OneToOneField(SymptomReport, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    advice = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(
        max_length=10,
        choices=[("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")],
        default="LOW"
    )

    def __str__(self):
        return f"Prediction for {self.symptom_report.student.user.username}: {self.disease}"
