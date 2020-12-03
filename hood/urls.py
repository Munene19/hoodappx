from django.urls import path
from . import views

urlpatterns = [
    path('hoodinfo/<str:pk>/', views.hoodDetail, name='hood-info'),
    path('postcreate/', views.postCreate, name='post-create'),
]