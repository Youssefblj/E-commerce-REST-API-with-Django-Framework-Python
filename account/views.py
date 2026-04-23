from datetime import timedelta, datetime
import django
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import signupSerializer, UserSerializer
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status   
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.core.mail import EmailMessage,send_mail


@api_view(['POST'])
def register(request):
    data = request.data
    user =signupSerializer(data=data)
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(first_name=data['first_name'], 
                                       last_name=data['last_name'],
                                       email=data['email'],
                                        username=data['email'],
                                       password= make_password(data['password']),
                                       )
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data
    user.first_name = data['first_name']
    user.last_name = data['last_name']  
    user.email = data['email']
    user.username = data['email']
    if data['password'] != '':  
        user.password = make_password(data['password'])
    user.save()
    serializer = signupSerializer(user, many=False)
    return Response(serializer.data)

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return f"{protocol}://{host}".format(protocol=protocol, host=host)

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    token = get_random_string(40)
    expired_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_token = token
    user.profile.reset_password_expire = expired_date
    user.profile.save()
    link ="http://localhost:8000/api/reset-password/{token}".format(token=token)
    body= 'your password reset link is {link}'.format(link=link)
    send_mail(
        'Password Reset from E-market',
        body,
        "noreply@emarket.com",
       [data['email']]
    )
    return Response({'details': 'Password reset link sent to your {email}'.format(email=[data['email']])})


@api_view(['POST'])
def reset_password(request, token):     
    data = request.data
    user = get_object_or_404(User, profile__reset_token=token)
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirm_password']:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    user.password = make_password(data['password'])
    user.profile.reset_token = ''
    user.profile.reset_password_expire = None   
    user.save()
    user.profile.save()
   
    return Response({'details': 'Password reset done '})
