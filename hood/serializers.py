from rest_framework import serializers
from .models import Neighborhood, Post, Profile

class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Neighborhood
        fields = '__all__' 

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields=['description', 'post_image', 'categories']

class ProfileSerializer(serializers.ModelSerializer):
    neighbourhood = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['profile_pic', 'idNo', 'neighbourhood', 'status', 'user'] 

