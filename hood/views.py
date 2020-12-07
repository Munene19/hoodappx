from django.contrib.auth.models import User
from django.shortcuts import render
from hood.models import Post, Profile, Neighborhood, Business, Vacanthouses
from rest_framework import viewsets, permissions, status
from .serializers import *
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Profile, Neighborhood, Post
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from .permissions import IsAdminOrReadOnly
from django.http import JsonResponse



def index(request):
    posts=Post.objects.all()
    return render(request, 'index.html')

class IsAssigned(permissions.BasePermission): 
    """
    Only person who assigned has permission
    """

    def has_object_permission(self, request, view, obj):
		# check if user who launched request is object owner 
        if obj.assigned_to == request.user: 
            return True

        return False
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAuthenticated]

class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)


    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def patch(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

def joinhood(request, id):
    current_user = request.user
    form = NeighborhoodForm() 
    
    if request.method == 'POST':
        form = NeighborhoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighborhood = form.save(commit=False)
            return(neighborhood)
            neighborhood.user_id =request.user.id
            neighborhood.save()

        return redirect(index)

    else:
        form = NeighborhoodForm()                    
        
    return render({"user": current_user, "form": form}) 

class HoodList(APIView):
    def get(self,request,format = None):
        all_hoods = Neighborhood.objects.all()
        serializerdata = HoodSerializer(all_hoods,many = True)
        return Response(serializerdata.data)

class PostList(APIView):
    def post(self, request, format=None):
        serializerdata=PostSerializer(data=request.data)
        if serializerdata.is_valid():
            serializerdata.save()
            return Response(serializerdata.data, status.HTTP_201_CREATED)
        return Response(serializerdata.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

class VacanthouseViewSet(viewsets.ModelViewSet):
    queryset = Vacanthouses.objects.all()
    serializer_class = VacanthousesSerializer

          
@api_view(['GET'])
def hoodDetail(request, pk):
    neighborhoods = Neighborhood.objects.get(id=pk)
    serializer = NeighborhoodSerializer(neighborhoods)
    return Response(serializer.data)


@permission_classes([IsAdminUser])
class NeighborhoodViewSet(viewsets.ModelViewSet):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer



