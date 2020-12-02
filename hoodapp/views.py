from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Post, Profile, Neighborhood, Business
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, UserRegistrationSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

def index(request):
    posts=Post.objects.all()
    return render(request, 'index.html')
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAuthenticated]


