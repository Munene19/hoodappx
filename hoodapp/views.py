from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Post, Profile, Neighborhood, Business
from rest_framework import viewsets
from rest_framework import permissions, status
from .serializers import UserSerializer, UserRegistrationSerializer, HoodSerializer, PostSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import Profile, Neighborhood, Post
from rest_framework.response import Response
from rest_framework.views import APIView

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

class HoodList(APIView):
    def get(self,request,format = None):
        all_hoods = Neighborhood.objects.all()
        serializerdata = HoodSerializer(all_hoods,many = True)
        return Response(serializerdata.data)

class PostList(APIView):
    def get(self, request, format=None):
        serializerdata=PostSerializer(data=request.data)
        if serializerdata.is_valid():
            serializerdata.save()
            return Response(serializerdata.data, status.HTTP_201_CREATED)
        return Response(serializerdata.errors, status=status.HTTP_400_BAD_REQUEST)