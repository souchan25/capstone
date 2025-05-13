from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, SymptomReport, PredictionRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'school_id', 'date_of_birth', 'share_data_consent']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Student
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 
                 'school_id', 'date_of_birth', 'share_data_consent']
    
    def create(self, validated_data):
        # Create the User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        # Create the Student profile
        student = Student.objects.create(
            user=user,
            school_id=validated_data['school_id'],
            date_of_birth=validated_data.get('date_of_birth'),
            share_data_consent=validated_data.get('share_data_consent', False)
        )
        
        # Return the user object (needed for token generation in the view)
        return user

class SymptomReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomReport
        fields = ['id', 'student', 'symptoms', 'created_at', 'input_method']
        read_only_fields = ['student', 'created_at']
    
    def create(self, validated_data):
        # Set the student to the current user's student profile
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                student = Student.objects.get(user=request.user)
                validated_data['student'] = student
            except Student.DoesNotExist:
                raise serializers.ValidationError("User does not have a student profile")
        
        return super().create(validated_data)

class PredictionRecordSerializer(serializers.ModelSerializer):
    symptom_report = SymptomReportSerializer(read_only=True)
    
    class Meta:
        model = PredictionRecord
        fields = ['id', 'symptom_report', 'disease', 'confidence_score', 
                 'advice', 'created_at', 'severity']
        read_only_fields = ['created_at']

class SymptomInputSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    input_method = serializers.ChoiceField(
        choices=["CHAT", "FORM"],
        default="FORM"
    )

class ConsentUpdateSerializer(serializers.Serializer):
    share_data_consent = serializers.BooleanField()