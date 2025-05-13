from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import logging

# Configure logger
logger = logging.getLogger(__name__)

class CustomAuthToken(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        try:
            if isinstance(request.data, dict):
                username = request.data.get('username', '')
                password = request.data.get('password', '')
            else:
                # Try to handle the request as form data
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                
            # Log attempt (without password)
            logger.info(f"Auth attempt with username: {username}")
            
            if not username or not password:
                logger.warning("Missing username or password")
                return Response({
                    "error": "Please provide both username and password"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            
            if not user:
                logger.warning(f"Invalid credentials for user: {username}")
                return Response({
                    "error": "Invalid credentials"
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Generate or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            logger.info(f"User {username} authenticated successfully")
            
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "username": user.username
            })
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return Response({
                "error": f"Authentication error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
